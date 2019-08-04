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
from knowledge.utils.knowledge_store_utils import generate_knowledge_store_published_message
from integrations.utils.slack_utils import trigger_knowledge_store_broadcast_activity
from integrations.constants import SLACK

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
        self.slug = custom_slugify(self.name, offset=30)
        super(KnowledgeStore, self).save(*args, **kwargs)

    @property
    def knowledge_store_published_message(self):
        return generate_knowledge_store_published_message(self)

    def __str__(self):
        return "{0}".format(self.name)


class Packet(RowInformation):
    """
    Helps Users create bundles or packets of knowledge resources
    """
    name = models.CharField(max_length=100, blank=False, null=False)
    slug = models.CharField(max_length=100, null=True, blank=True)
    resources = models.ManyToManyField(to=KnowledgeStore, related_name='packet')
    created_by = models.ForeignKey(to=Hustler, related_name='packet', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'packet'

    def save(self, *args, **kwargs):
        self.slug = custom_slugify(self.name, offset=30)
        super(Packet, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.name)


def broadcast_resource_published_message(sender, instance, action, **kwargs):
    """
    Every time a row is created in the through table between KnowledgeStore and Category
    this signal will fire and publish itself on the broadcast network (Slack/Basecamp)

    Currently, this event is being triggered even when post creation in the edit mode if we are
    adding more categories to a KnowledgeStore resource
    """
    # import code; code.interact(local=locals())
    logger.debug(action)

    # different action types are post_add, pre_add, pre_remove, post_remove, pre_clear, post_clear
    # https://docs.djangoproject.com/en/dev/ref/signals/#m2m-changed
    if action != 'post_add':
        return

    # broadcast_message = instance.knowledge_store_published_message
    # logger.debug(broadcast_message.upper())

    resource_object_id = instance.id
    logger.debug(resource_object_id)

    try:
        trigger_knowledge_store_broadcast_activity(knowledge_store_object_id=resource_object_id,
                                                   broadcast_channels=[SLACK])
    except Exception as e:
        # handle this better
        logger.error("Boardcasting services failed")


m2m_changed.connect(broadcast_resource_published_message, sender=KnowledgeStore.categories.through)
