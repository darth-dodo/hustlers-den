# third party imports
import os
import sys
import logging

# django imports
from django.db import transaction

# project level imports
from utils.services.base_service import BaseService
from utils.hustlers_den_exceptions import HustlersDenValidationError
from utils.auth_utils import generate_hustler_password
from django.utils.text import slugify
from knowledge.models import Category

# app level imports
from hustlers.models import User, Hustler
from hustlers.api.serializers import HustlerSerializer

logger = logging.getLogger(__name__)


class HustlerCreation(BaseService):
    """
    validations
    - checks if the email is present as Django User

    execution
    - creates django user
    - creates hustler object
    - attaches interests to the hustler object
    - [todo] if created by an active Admin User


    a = {
            "username": "test@gmail.com",
            "first_name": "Test",
            "last_name": "Apples",
            "is_superuser": False,
            "interests": ["Python", "Django", "Machine Learning", "Ruby"],
            "request_user": "Django User object"
        }

    return :bool: Service success status
    return :HustlersDenValidationError: if case of errors and `raise_errors` mode

    """
    def __init__(self, context):

        super().__init__()
        self.__context = context
        self.__username = context.get('username')
        self.__first_name = context.get('first_name')
        self.__last_name = context.get('last_name')
        self.__is_superuser = context.get('is_superuser')
        self.__interests = context.get('interests')

        self.__django_user_object = None
        self.__hustler_object = None

        self.service_response_data = dict()

        # todo: figure out how to access request user
        self.__current_user = context.get('request_user')

    def validate(self, raise_errors=False):
        self.__validate_django_user_and_hustler_pairing()

        if self.__is_superuser:
            self.__validate_superuser_creation()

        return super().validate(raise_errors)

    @transaction.atomic()
    def execute(self, raise_errors=False):

        # run validations if not run already, return False if validations weren't successful
        super().execute(raise_errors)
        if not self.is_valid: return self.is_valid

        self.__django_user_object = self.__get_or_create_django_user_object()
        self.__hustler_object = self.__create_hustler_object()

        if self.__interests:
            self.__attach_hustler_interests()

        if self.__is_superuser:
            self.__mark_as_superuser()

        self.__set_service_response_data()

        return self.is_valid

    # private methods

    # validators
    def __validate_django_user_and_hustler_pairing(self):
        if not self.__username:
            self.errors.append("Username cannot be blank!")

        try:
            user_object = User.objects.get(username=self.__username)
            if hasattr(user_object, 'hustler'):
                self.errors.append("Hustler is already present in the system!")
        except User.DoesNotExist:
            pass

    def __validate_superuser_creation(self):
        if not self.__current_user.user.hustler.superuser_access:
            self.errors.append("You need to be a SuperUser yourself to create another super user!")

    # executors
    def __get_or_create_django_user_object(self):
        try:
            django_user = User.objects.get(username=self.__username)
        except User.DoesNotExist:
            self.__generated_password = generate_hustler_password()

            django_user = User()
            django_user.username = self.__username
            django_user.email = self.__username
            django_user.first_name = self.__first_name
            django_user.last_name = self.__last_name

            django_user.set_password(self.__generated_password)
            django_user.save()

        return django_user

    def __create_hustler_object(self):
        hustler = Hustler()
        hustler.django_user = self.__django_user_object
        hustler.created_by = hustler.modified_by = self.__current_user.hustler

        hustler.save()

        return hustler

    def __mark_as_superuser(self):
        self.__django_user_object.is_superuser = True
        self.__django_user_object.save()

    def __attach_hustler_interests(self):
        interest_slugs = [slugify(current_interest) for current_interest in self.__interests]
        interest_objects = list(Category.objects.slug_in(interest_slugs))
        self.__hustler_object.interests.add(*interest_objects)


    def __set_service_response_data(self):
        user_data = HustlerSerializer(self.__hustler_object).data
        user_data.update({"password": self.__generated_password})
        self.service_response_data = user_data
