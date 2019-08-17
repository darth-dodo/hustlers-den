import logging

# framework level libraries
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_filters import rest_framework as filters


# project level imports
from utils.views_utils import eager_load

# app level imports
from knowledge.models import KnowledgeStore, Category, ExpertiseLevel, MediaType

# api level imports
from knowledge.api.serializers import CategorySerializer, MediaTypeSerializer, ExpertiseLevelSerializer, \
    KnowledgeStoreSerializer

from knowledge.api.pagination import KnowledgeListPagination

logger = logging.getLogger(__name__)


class ReadOnlyKnowledgeAbstractViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Abstract Parent Readonly ViewSet
    """
    serializer_class = None
    authentication_classes = [JSONWebTokenAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = []
    filter_fields = []
    ordering_fields = []
    ordering = []
    queryset = None
    pagination_class = KnowledgeListPagination

    class Meta:
        abstract = True


class CategoryViewSet(ReadOnlyKnowledgeAbstractViewSet):
    """
    handles ViewSet for Category Serializer
    """
    serializer_class = CategorySerializer
    filter_fields = ['id', 'name', 'slug']
    search_fields = ['name', 'slug']
    queryset = Category.objects.all()


class MediaTypeViewSet(ReadOnlyKnowledgeAbstractViewSet):
    """
    handles ViewSet for MediaType Serializer
    """
    serializer_class = MediaTypeSerializer
    filter_fields = ['id', 'name', 'slug']
    search_fields = ['name', 'slug']
    queryset = MediaType.objects.all()


class ExpertiseLevelViewSet(ReadOnlyKnowledgeAbstractViewSet):
    """
    handles ViewSet for ExpertiseLevel Serializer
    """
    serializer_class = ExpertiseLevelSerializer
    filter_fields = ['id', 'name', 'slug']
    search_fields = ['name', 'slug']
    queryset = ExpertiseLevel.objects.active()


# ToDo: Create abstract viewset with serializer.save() for create and update
class KnowledgeStoreViewSet(viewsets.ModelViewSet):
    """
    handles ViewSet for KnowledgeStore Serializer

    sample post

            {
                "media_type": 2,
                "categories": [
                    1,
                    3,
                    5,
                    6
                ],
                "expertise_level": 1,
                "name": "Python Basics",
                "url": "https://learnpythonthehardway.org",
                "description": "",
                "difficulty_sort": 1
            }
    """
    authentication_classes = [JSONWebTokenAuthentication,
                              SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = KnowledgeStoreSerializer
    filter_fields = ['id', 'name', 'slug']
    search_fields = ['name', 'slug']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    queryset_class = KnowledgeStore
    queryset = queryset_class.objects.active()

    @eager_load
    def get_queryset(self):
        logger.debug('Data: {0} | User: {1}'.format(self.request.data, self.request.user))
        return self.queryset_class.objects.active()

    def perform_create(self, serializer):
        logger.debug('Data: {0} | User: {1}'.format(self.request.data, self.request.user))
        hustler_obj = self.request.user.hustler
        serializer.save(created_by=hustler_obj, modified_by=hustler_obj)

    def perform_update(self, serializer):
        logger.debug('Data: {0} | User: {1}'.format(self.request.data, self.request.user))
        serializer.save(modified_by=self.request.user.hustler)
