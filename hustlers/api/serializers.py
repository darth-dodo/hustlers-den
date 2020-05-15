from rest_framework import serializers
from hustlers.models import Hustler

# TODO create a Recursive Serializer for created_by
# https://github.com/encode/django-rest-framework/pull/2459


class HustlerSerializer(serializers.ModelSerializer):
    """
    Hustler model serializer using actual fields and properties to 
    get Django User specific data
    """
    from knowledge.api.serializers import CategorySerializer
    interests = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Hustler
        fields = ('interests', 'created_by', 'created_at',
                  'active', 'full_name', 'email', 'username', 'superuser_access')