# third party imports
import os
import logging
import sys

# django imports
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


# project level imports
from den.utils.model_utils import RowInformation, custom_slugify
from hustlers.models import Hustler
from integrations.utils.slack_utils import post_message_to_slack_channel

# app level imports
from knowledge.managers import CategoryManager, KnowledgeStoreManager, MediaTypeManager, ExpertiseLevelManager

# TODO data integrity for active hustler check and hustler abstract model

logger = logging.getLogger(__name__)

class Category(RowInformation):
    """
    database, python, django, rails ,flask etc
    """
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True)
    slug = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(to=Hustler,
                                   related_name='categories',
                                   on_delete=models.SET_NULL,
                                   null=True)

    objects = CategoryManager()

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.name)


class MediaType(RowInformation):
    """
    Conf video, article, interactive tutorial
    """
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True)
    slug = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(to=Hustler,
                                   related_name='media_types',
                                   on_delete=models.SET_NULL,
                                   null=True)

    objects = MediaTypeManager()

    class Meta:
        db_table = 'media_type'

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.slug = slugify(self.name)
        super(MediaType, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.name)


class ExpertiseLevel(RowInformation):
    """
    Flexible for adding different sets of experience levels
    eg. Beginner, Intermediate, Advanced
    eg. Novice, Apprentice, Master, Expert
    """
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True)
    slug = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(to=Hustler,
                                   related_name='expertise_levels',
                                   on_delete=models.SET_NULL,
                                   null=True)

    objects = ExpertiseLevelManager()

    class Meta:
        db_table = 'expertise_level'

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.slug = slugify(self.name)
        super(ExpertiseLevel, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.name)


class KnowledgeStore(RowInformation):
    """
    Stores information mapped across categories and difficulty levels as well as internal ranking
    """
    name = models.CharField(max_length=100, blank=False, null=False)
    url = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True)

    # internal ordering for sorting resources instead knowledge store for a particular expertise level
    difficulty_sort = models.PositiveIntegerField(default=1)

    # associations
    expertise_level = models.ForeignKey(to=ExpertiseLevel,
                                        related_name='knowledge_store',
                                        on_delete=models.SET_NULL,
                                        null=True)

    media_type = models.ForeignKey(to=MediaType,
                                   related_name='knowledge_store',
                                   on_delete=models.SET_NULL,
                                   null=True)

    created_by = models.ForeignKey(to=Hustler,
                                   related_name='knowledge_store',
                                   on_delete=models.SET_NULL,
                                   null=True)

    categories = models.ManyToManyField(to=Category,
                                        related_name='knowledge_store')

    slug = models.CharField(max_length=100, null=True, blank=True)

    objects = KnowledgeStoreManager()

    class Meta:
        db_table = 'knowledge_store'

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        self.slug = custom_slugify(self.name, offset=30)
        super(KnowledgeStore, self).save(*args, **kwargs)

    @property
    def knowledge_store_published_message(self):
        obj = KnowledgeStore.objects.get(id=self.id)
        hustler_name = obj.created_by.first_name if obj.created_by.first_name else obj.created_by.email
        resource_name = obj.name
        resource_url = obj.url
        categories = list(obj.categories.values_list('name', flat=True))

        message = "{0}".format(resource_name)

        if resource_url:
            message = "{0} ({1})".format(message, resource_url)

        if categories:
            categories_str = ', '.join(categories)
            message = "{0} across categories *{1}*".format(message, categories_str)

        if hustler_name:
            message = "{0} has been posted by {1}".format(message, hustler_name)

        return message



    def __str__(self):
        return "{0}".format(self.name)

def broadcast_resouce_published_message(sender, instance, **kwargs):

        broadcast_message = instance.knowledge_store_published_message
        logger.debug(broadcast_message.upper())

        try:
            post_message_to_slack_channel(broadcast_message)
        except Exception as e:
            # handle this better
            logger.error("Boardcasting services failed")


m2m_changed.connect(broadcast_resouce_published_message, sender=KnowledgeStore.categories.through)
