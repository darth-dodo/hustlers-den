# framework level libraries
from django.db.models import Q
from django.db.models import  Case, IntegerField, Value, When
import itertools
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
    )

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
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
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
    search_fields = []
    ordering_fields = []
    ordering = []
    queryset = Category.objects.all()

    # def get_queryset(self):
    #     return Category.objects.active()


class MediaTypeViewSet(ReadOnlyKnowledgeAbstractViewSet):
    """
    handles ViewSet for MediaType Serializer
    """
    serializer_class = MediaTypeSerializer
    filter_fields = ['id', 'name', 'slug']
    search_fields = []
    ordering_fields = []
    ordering = []
    queryset = MediaType.objects.all()


class ExpertiseLevelViewSet(ReadOnlyKnowledgeAbstractViewSet):
    """
    handles ViewSet for ExpertiseLevel Serializer
    """
    serializer_class = ExpertiseLevelSerializer
    filter_fields = ['id', 'name', 'slug']
    search_fields = []
    ordering_fields = []
    ordering = []
    queryset = ExpertiseLevel.objects.active()


class KnowledgeStoreViewSet(ReadOnlyKnowledgeAbstractViewSet):
    """
    handles ViewSet for KnowledgeStore Serializer
    """
    serializer_class = KnowledgeStoreSerializer
    filter_fields = ['id', 'name', 'slug']
    search_fields = []
    ordering_fields = []
    ordering = []
    queryset = KnowledgeStore.objects.active()
