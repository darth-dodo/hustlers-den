# third party imports

# django imports
from django.db import models
from django.utils.text import slugify

# project level imports
from den.utils.model_utils import RowInformation, custom_slugify
from hustlers.models import Hustler

# app level imports

# TODO data integrity for active hustler check and hustler abstract model


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

    class Meta:
        db_table = 'knowledge_store'

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        self.slug = custom_slugify(self.name, offset=30)
        super(KnowledgeStore, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.name)
