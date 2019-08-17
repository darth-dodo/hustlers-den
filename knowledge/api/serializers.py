# django imports
from rest_framework import serializers


# project level imports
from utils.serializers_utils import EagerLoadingSerializerMixin

# app level imports
from knowledge.models import KnowledgeStore, Category, MediaType, ExpertiseLevel
from hustlers.models import Hustler


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryFormSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', )


class MediaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaType
        fields = '__all__'


class MediaTypeFormSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = MediaType
        fields = ('id', 'name', )


class ExpertiseLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseLevel
        fields = '__all__'


class ExpertiseLevelFormSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseLevel
        fields = ('id', 'name', )


class KnowledgeStoreSerializer(serializers.ModelSerializer, EagerLoadingSerializerMixin):

    expertise_level = serializers.PrimaryKeyRelatedField(queryset=ExpertiseLevel.objects.active())
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.active())
    media_type = serializers.PrimaryKeyRelatedField(queryset=MediaType.objects.active())
    created_by = serializers.PrimaryKeyRelatedField(queryset=Hustler.objects.all(), required=False)
    modified_by = serializers.PrimaryKeyRelatedField(many=True, queryset=Hustler.objects.all(), required=False)

    _SELECT_RELATED_FIELDS = ['expertise_level', 'media_type', 'created_by', 'modified_by']
    _PREFETCH_RELATED_FIELDS = ['categories']

    class Meta:
        model = KnowledgeStore
        fields = (
                  'id', 'created_by', 'modified_by', 'media_type', 'categories', 'expertise_level', 'name',
                  'url', 'description', 'difficulty_sort', 'slug', 'created_at', 'modified_at',
                  )