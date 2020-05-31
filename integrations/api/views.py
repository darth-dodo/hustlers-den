import logging

from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from knowledge.api.serializers import (
    CategoryFormSerilaizer,
    ExpertiseLevelFormSerilaizer,
    MediaTypeFormSerilaizer,
)
from knowledge.models import Category, ExpertiseLevel, MediaType

logger = logging.getLogger(__name__)


class IntegrationsAPIView(APIView):
    """
    Abstract Integrations APIView handling auth
    """

    serializer_class = None
    permission_classes = [IsAuthenticated]
    authentication_classes = [
        JSONWebTokenAuthentication,
        SessionAuthentication,
        BasicAuthentication,
    ]
    filter_backends = []
    search_fields = []
    filter_fields = []
    ordering_fields = []
    ordering = []
    queryset = None

    class Meta:
        abstract = True


class ExtensionFormData(IntegrationsAPIView):
    """
    Generates the data using which the chrome extension fills the dropdown
    """

    def get(self, request, format=None):
        """
        returns a JSON of active categories, expertise levels and media types from the db
        """

        logger.debug(
            "Data: {0} | User: {1}".format(self.request.data, self.request.user)
        )

        active_categories = Category.objects.active()
        active_expertise_levels = ExpertiseLevel.objects.active()
        active_media_types = MediaType.objects.active()

        data = {
            "categories": CategoryFormSerilaizer(active_categories, many=True).data,
            "media_types": MediaTypeFormSerilaizer(active_media_types, many=True).data,
            "expertise_levels": ExpertiseLevelFormSerilaizer(
                active_expertise_levels, many=True
            ).data,
        }

        return Response(data, status=HTTP_200_OK)
