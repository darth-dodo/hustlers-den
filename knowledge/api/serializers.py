# third party imports
import os
import sys
import logging

# django imports
from rest_framework import serializers


# project level imports
from utils.serializers_utils import EagerLoadingSerializerMixin
from utils.custom_error_handlers import HustlersDenValidationError
from hustlers.models import Hustler

# app level imports
from knowledge.models import KnowledgeStore, Category, MediaType, ExpertiseLevel


logger = logging.getLogger(__name__)


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
    # modified_by = serializers.PrimaryKeyRelatedField(queryset=Hustler.objects.all(), required=False)
    modified_by = serializers.PrimaryKeyRelatedField(queryset=Hustler.objects.all())

    categories_data = serializers.SerializerMethodField()

    _SELECT_RELATED_FIELDS = ['expertise_level', 'media_type', 'created_by', 'modified_by']
    _PREFETCH_RELATED_FIELDS = ['categories']

    class Meta:
        model = KnowledgeStore
        fields = (
                  'id', 'modified_by', 'media_type', 'categories', 'expertise_level', 'name',
                  'url', 'description', 'difficulty_sort', 'slug',
                  'categories_data',
                  'created_by', 'created_at', 'modified_at', 'modified_by')

    def get_categories_data(self, obj):
        return [CategorySerializer(current_category).data for current_category in obj.categories.all()]

    # this won't be triggered as the modified by is not provided in the request body'
    # validations
    def validate_modified_by(self, value):
        import code; code.interact(local=locals())

        logger.debug("validation")

        request_object = self.context['request'].user

        if not hasattr(request_object, 'hustler'):
            raise HustlersDenValidationError("Please register for a Hustler account!")

        has_superuser_access = request_object.hustler.superuser_access

        # self just contains the current partial data
        if self.created_by != value and not has_superuser_access:
            raise HustlersDenValidationError("You are not authorized to perform this action!")

        return value
