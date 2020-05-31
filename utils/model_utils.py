from django.db import models
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string


def custom_slugify(data, suffix=True, offset=15):
    """
    Using django util methods create a slug.
    Append a random string at the end of the slug if necessary for making it unique
    """

    # slugify the source_field passed to the function
    new_slug = slugify(data)[:offset]

    if suffix:
        # get a random string of length 10
        random_str = get_random_string(length=10)

        # the new_slug and random_str is concatenated
        new_slug = "{0}-{1}".format(new_slug, random_str)

    return new_slug


class RowInformation(models.Model):
    """
    This class is used to maintain meta information such as is_active, created_at, modified_at
    This can  be inherited in other classes to avoid making repeated attributes
    """

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
