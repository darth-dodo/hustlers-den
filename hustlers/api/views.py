import sys
import os
import logging

from django.core.exceptions import FieldError
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.hustlers_den_exceptions import HustlersDenValidationError
from utils.views_utils import eager_load


logger = logging.getLogger(__name__)


class HustlerAbstractViewSet(viewsets.ModelViewSet):
    """

    """

    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = None
    queryset_class = None
    permission_field = 'created_by'

    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = []
    ordering_fields = []
    ordering = []

    class Meta:
        abstract = True

    @eager_load
    def get_queryset(self):
        """
        Overriding `get_queryset` to restrict edit access to non owners and non superusers
        :return:
        """
        hustler_obj = self.request.user.hustler

        if hustler_obj.superuser_access:
            queryset = self.queryset_class.all()
        else:
            try:
                required_filters = {self.permission_field: hustler_obj}
                queryset = self.queryset_class.filter(**required_filters)
            except FieldError:
                logger.error("Stack trace: {0} | Data: {1} | Message: {2}".format(
                    sys._getframe().f_code.co_name, locals(), "Field Error in Abstract Viewset"))
                raise HustlersDenValidationError()

        return queryset
