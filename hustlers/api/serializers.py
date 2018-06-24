from rest_framework import serializers

from hustlers.models import Hustler
from knowledge.api.serializers import CategorySerializer

# TODO create a Recursive Serializer for created_by
# https://github.com/encode/django-rest-framework/pull/2459


class HustlerSerializer(serializers.ModelSerializer):
    """
    Hustler model serializer using actual fields and properties to 
    get Django User specific data
    """
    interests = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Hustler
        fields = ('interests', 'created_by', 'created_at',
                  'active', 'full_name', 'email', 'username', 'superuser_access')

    @staticmethod
    def get_superuser_access(obj):
        return obj.django_user.is_superuser

    superuser_access = serializers.SerializerMethodField(read_only=True)