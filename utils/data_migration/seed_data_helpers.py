# third party imports


# django imports
from django.contrib.auth.models import Group, Permission, User
from django.utils.text import slugify


# project level imports
from hustlers.constants import ALL_PERMISSION_GROUPS
from hustlers.models import Hustler
from knowledge.models import Category, MediaType, ExpertiseLevel

# app level imports
from utils.data_migration.seed_data_constants import SEED_CATEGORIES, SEED_MEDIA_TYPES, SEED_EXPERTISE_LEVELS
from utils.hustlers_den_exceptions import HustlersDenBaseException


def get_or_create_groups():
    print("Creating Groups and attaching Permissions")
    for current_permission_group in ALL_PERMISSION_GROUPS:
        try:
            permission_group = Group.objects.get(name=current_permission_group)
        except Exception as e:
            print(e)
            permission_group = Group()
            permission_group.name = current_permission_group
            permission_group.save()
            non_delete_permissions = Permission.objects.exclude(codename__startswith='delete')
            permission_group.permissions.set(non_delete_permissions)
            permission_group.save()


def get_or_create_users_and_hustlers():
    """
    Wrapper for generating different types of users
    :return:
    """
    print("Creating Hustlers")
    create_admin_super_user()


def create_admin_super_user():
    """
    Get or create Admin Django User and Hustler object
    :return:
    """
    print("Creating Admin Hustler with Super User access")
    try:
        user = User.objects.get(username='admin@hden.com')
    except User.DoesNotExist:
        user = User()
        user.username = 'admin@hden.com'
        user.set_password('sharing-is-caring')
        user.is_staff = True
        user.is_superuser = True
        user.save()

        create_hustler(user)


def create_hustler(user_object):
    """
    Creates a Hustler object for a corresponding User object
    :param user_object:  User instance
    :return:
    """
    print("Creating Hustler object for {0}".format(user_object.username))
    hustler = Hustler()
    hustler.django_user = user_object
    hustler.save()


def get_admin_hustler():
    """
    Returns the Admin Hustler object or raise an Exception
    :return:
    """
    try:
        user_object = User.objects.get(username='admin@hden.com')
        if not hasattr(user_object, 'hustler'):
            raise HustlersDenBaseException("Hustler not present!")

    except User.DoesNotExist:
        raise HustlersDenBaseException("Django User is not present!")


def get_or_create_categories():
    """
    Gets or creates seed Categories as specified in the constants file
    :return:
    """
    print("Creating Categories")
    admin_hustler = get_admin_hustler()
    for current_category in SEED_CATEGORIES:
        category_slug = slugify(current_category)
        category, created = Category.objects.get_or_create(slug=category_slug,
                                                           name=current_category,
                                                           created_by=admin_hustler)


def get_or_create_expertise_levels():
    """
    Gets or creates seed Expertise Levels as specified in the constants file
    :return:
    """
    print("Creating Expertise Levels")
    admin_hustler = get_admin_hustler()
    for current_expertise_level in SEED_EXPERTISE_LEVELS:
        expertise_level_slug = slugify(current_expertise_level)
        expertise_level, created = ExpertiseLevel.objects.get_or_create(slug=expertise_level_slug,
                                                                        name=current_expertise_level,
                                                                        created_by=admin_hustler)


def get_or_create_media_types():
    """
    Gets or creates seed Media Types as specified in the constants file
    :return:
    """
    print("Creating Media Types")
    admin_hustler = get_admin_hustler()
    for current_media_type in SEED_MEDIA_TYPES:
        media_type_slug = slugify(current_media_type)
        media_type, created = MediaType.objects.get_or_create(slug=media_type_slug,
                                                              name=current_media_type,
                                                              created_by=admin_hustler)


def get_or_create_knowledge_resources():
    pass
