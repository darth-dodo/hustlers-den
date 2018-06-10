from django.db import models
from django.utils.text import slugify
# Create your models here.

from den.utils.model_utils import RowInformation


class Category(RowInformation):
    """
    database, python, django, rails ,flask etc
    """
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=100)

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.name)


class ExpertiseLevel(RowInformation):
    """
    Flexible for adding different sets of experience levels
    eg. Beginner, Intermediate, Advanced
    eg. Novice, Apprentice, Master, Expert
    """
    name = models.CharField(max_length=100, blank=False, null=False)
    slug = models.CharField(max_length=100)

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
    description = models.TextField(null=True, blank=True)

    expertise_level = models.ForeignKey(to=ExpertiseLevel,
                                        related_name='knowledge_store',
                                        on_delete=models.SET_NULL,
                                        null=True)

    # internal ordering for sorting resources instead knowledge store for a particular expertise level
    difficulty_sort = models.PositiveIntegerField(default=1)

    categories = models.ManyToManyField(to=Category, related_name='knowledge_store')

    class Meta:
        db_table = 'knowledge_store'

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(KnowledgeStore, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.name)