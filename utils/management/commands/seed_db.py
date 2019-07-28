from django.core.management.base import BaseCommand
from django.db import transaction
from utils.data_migration.seed_data_helpers import get_or_create_groups, get_or_create_users_and_hustlers, \
    get_or_create_categories, get_or_create_expertise_levels, get_or_create_media_types


class Command(BaseCommand):
    help = 'Seed database creation'

    def handle(self, *args, **kwargs):
        get_or_create_groups()
        get_or_create_users_and_hustlers()
        get_or_create_categories()
        get_or_create_expertise_levels()
        get_or_create_media_types()
