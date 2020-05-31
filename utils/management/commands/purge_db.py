from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Remove ALL data"

    def handle(self, *args, **kwargs):
        pass
