import logging

from rest_framework import serializers

from hustlers.models import Hustler
from knowledge.models import Category, ExpertiseLevel, KnowledgeStore, MediaType
from utils.serializers_utils import EagerLoadingSerializerMixin

logger = logging.getLogger(__name__)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
        )


class CategoryFormSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class MediaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaType
        fields = "__all__"


class MediaTypeFormSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = MediaType
        fields = (
            "id",
            "name",
        )


class ExpertiseLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseLevel
        fields = "__all__"


class ExpertiseLevelFormSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseLevel
        fields = (
            "id",
            "name",
        )


class KnowledgeStoreSerializer(
    serializers.ModelSerializer, EagerLoadingSerializerMixin
):

    expertise_level = serializers.PrimaryKeyRelatedField(
        queryset=ExpertiseLevel.objects.active()
    )
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.active()
    )
    media_type = serializers.PrimaryKeyRelatedField(queryset=MediaType.objects.active())
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=Hustler.objects.all(), required=False
    )
    modified_by = serializers.PrimaryKeyRelatedField(
        queryset=Hustler.objects.all(), required=False
    )

    categories_data = serializers.SerializerMethodField()

    _SELECT_RELATED_FIELDS = [
        "expertise_level",
        "media_type",
        "created_by",
        "modified_by",
    ]
    _PREFETCH_RELATED_FIELDS = ["categories"]

    class Meta:
        model = KnowledgeStore
        fields = (
            "id",
            "modified_by",
            "media_type",
            "categories",
            "expertise_level",
            "name",
            "url",
            "description",
            "difficulty_sort",
            "slug",
            "categories_data",
            "created_by",
            "created_at",
            "modified_at",
            "modified_by",
        )

    def get_categories_data(self, obj):
        return CategoryMiniSerializer(obj.categories.all(), many=True).data
