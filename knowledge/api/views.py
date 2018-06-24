# framework level libraries
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_filters import rest_framework as filters


# project level imports

# app level imports
from knowledge.models import KnowledgeStore, Category, ExpertiseLevel, MediaType

# api level imports
from knowledge.api.serializers import CategorySerializer, MediaTypeSerializer, ExpertiseLevelSerializer, \
    KnowledgeStoreSerializer

from knowledge.api.pagination import KnowledgeListPagination


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

    # def get_queryset(self):
    #     return Category.objects.active()


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


class KnowledgeStoreViewSet(ReadOnlyKnowledgeAbstractViewSet):
    """
    handles ViewSet for KnowledgeStore Serializer
    """
    serializer_class = KnowledgeStoreSerializer
    filter_fields = ['id', 'name', 'slug']
    search_fields = ['name', 'slug']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    queryset = KnowledgeStore.objects.active()
