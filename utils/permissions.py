import os
import sys
import logging

from rest_framework.permissions import BasePermission, SAFE_METHODS

from utils.hustlers_den_exceptions import HustlersPermissionDenied

from hustlers.models import Hustler

logger = logging.getLogger(__name__)


class IsOwnerOrSuperUser(BasePermission):

    def has_object_permission(self, request, view, obj):

        logger.debug(request, view, obj)

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        hustler_obj = request.user.hustler

        # SuperUsers have universal access
        if hustler_obj.superuser_access:
            return True

        # Only SuperUsers can edit other Hustlers
        if isinstance(obj, Hustler) and obj != hustler_obj:
            raise HustlersPermissionDenied("You cannot edit other Hustlers!")

        # Only SuperUsers can edit objects created by other Hustlers
        if not obj.created_by == hustler_obj:
            raise HustlersPermissionDenied("You cannot edit if you are not the owner")
