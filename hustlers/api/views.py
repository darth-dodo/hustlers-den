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
from utils.permissions import IsOwnerOrSuperUser

from hustlers.models import Hustler
from hustlers.api.serializers import HustlerSerializer


logger = logging.getLogger(__name__)


class HustlerAbstractViewSet(viewsets.ModelViewSet):
    """

    """

    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]

    serializer_class = None
    queryset_class = None
    queryset = None

    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = []
    ordering_fields = []
    ordering = []

    class Meta:
        abstract = True

    @eager_load
    def get_queryset(self):
        """
        Overriding `get_queryset`
        :return:
        """

        """
        The flow is as follows:
        ** get_queryset -> get_object -> check_permissions **
        
        if we restrict the queryset for non superusers as just their filter, running 
        `get_object` will return a 404 and `check_permissions` shall never be triggered 

        ```
        if hustler_obj.superuser_access:
            queryset = self.queryset_class.objects.all()
        else:
            queryset = self.queryset_class.objects.filter(django_user=hustler_obj)
        ```
            
        as compared to other areas where we are letting the list show up entirely in the qs but prevent changed 
        based on the `IsOwnerOrSuperUser` permission
        
        For more details check out the code for `GenericViewSet`
        
        This would have made sense if we wanted to return a 404/ghost so that other users can't even view
        """

        queryset = self.queryset_class.objects.all()
        return queryset

    def perform_update(self, serializer):
        logger.debug('Data: {0} | User: {1}'.format(self.request.data, self.request.user))
        serializer.save(modified_by=self.request.user.hustler)


class HustlerViewSet(HustlerAbstractViewSet):
    """

    """
    queryset_class = Hustler
    queryset = queryset_class.objects.all()
    serializer_class = HustlerSerializer
