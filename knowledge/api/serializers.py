from rest_framework import serializers


from knowledge.models import KnowledgeStore, Category, MediaType, ExpertiseLevel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MediaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaType
        fields = '__all__'


class ExpertiseLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseLevel
        fields = '__all__'


class KnowledgeStoreSerializer(serializers.ModelSerializer):
    expertise_level = ExpertiseLevelSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    media_type = MediaTypeSerializer(read_only=True)
    # created_by = HustlerSerializer(read_only=True)

    class Meta:
        model = KnowledgeStore
        fields = '__all__'
