import os
import sys
import logging

# django imports
from rest_framework import serializers

# project level imports
from knowledge.models import Category

# app level imports
from hustlers.models import Hustler


# TODO create a Recursive Serializer for created_by
# https://github.com/encode/django-rest-framework/pull/2459


class HustlerMiniSerializer(serializers.ModelSerializer):
    """
    Lite weight Hustler Serializer
    """

    user_id = serializers.SerializerMethodField()

    class Meta:
        model = Hustler
        fields = ('full_name', 'email', 'username', 'superuser_access', 'user_id')

    def get_user_id(self, obj):
        return obj.django_user_id


class HustlerSerializer(serializers.ModelSerializer):
    """
    Hustler model serializer using actual fields and properties to 
    get Django User specific data
    """
    interests = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.active())
    user_id = serializers.SerializerMethodField()
    created_by_data = serializers.SerializerMethodField()
    interests_meta_data = serializers.SerializerMethodField()

    class Meta:
        model = Hustler
        fields = ('interests', 'created_by', 'created_at', 'created_by_data',
                  'active', 'full_name', 'email', 'username', 'superuser_access', 'user_id', 'interests_meta_data')

    def get_user_id(self, obj):
        return obj.django_user_id

    def get_created_by_data(self, obj):
        return HustlerMiniSerializer(obj.created_by).data

    def get_interests_meta_data(self, obj):
        from knowledge.api.serializers import CategoryMiniSerializer
        return CategoryMiniSerializer(obj.interests.active(), many=True).data
