from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from knowledge.models import Category


class Hustler(models.Model):
    """
    One to One with the Django User model
    Each hustler can have interests in zero or more categories
    """
    bio = models.TextField(max_length=500, blank=True)

    django_user = models.OneToOneField(to=User,
                                       primary_key=True,
                                       related_name='hustler',
                                       on_delete=models.PROTECT)

    created_by = models.ForeignKey(to='self',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)

    interests = models.ManyToManyField(to=Category,
                                       blank=True,
                                       related_name='hustlers')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hustlers'

    @classmethod
    def from_db(cls, db, field_names, values):
        new = super(Hustler, cls).from_db(db, field_names, values)
        # cache value went from the base
        new._updated_django_user_id = values[field_names.index('django_user_id')]
        return new

    def save(self, *args, **kwargs):

        if hasattr(self, '_updated_django_user_id'):

            if (not self._state.adding
                and self._updated_django_user_id is not None and
                        self._updated_django_user_id != self.django_user_id):

                raise ValidationError("You cannot reassign Hustler to different User!")

        super(Hustler, self).save(*args, **kwargs)

    @property
    def username(self):
        return '{0}'.format(self.django_user.username)

    @property
    def first_name(self):
        return '{0}'.format(self.django_user.first_name)

    @property
    def last_name(self):
        return '{0}'.format(self.django_user.last_name)

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    @property
    def email(self):
        return '{0}'.format(self.django_user.email)

    @property
    def active(self):
        return '{0}'.format(self.django_user.is_active)

    def __str__(self):
        return "{0}".format(self.username)


# signals
@receiver(post_save, sender=User)
def save_hustler(sender, instance, **kwargs):
    """
    Saving/Updating Hustler every time user object is changed for syncing updated_at
    """
    if hasattr(instance, 'hustler'):
        instance.hustler.save()
