from django.core.management.base import BaseCommand

from hustlers.constants import ALL_PERMISSION_GROUPS
from hustlers.models import Hustler, User
from hustlers.utils.permission_utils import Group
from knowledge.models import Category, ExpertiseLevel, KnowledgeStore, MediaType, Packet


class Command(BaseCommand):
    help = "Remove ALL data"

    def handle(self, *args, **kwargs):
        print(f"Deleting Packets")
        print(Packet.objects.all().delete())

        print(f"Deleting Knowledge Stores")
        print(KnowledgeStore.objects.all().delete())

        print(f"Deleting Categories")
        print(Category.objects.all().delete())

        print(f"Deleting Media Types")
        print(MediaType.objects.all().delete())

        print(f"Deleting Expertise Levels")
        print(ExpertiseLevel.objects.all().delete())

        print(f"Deleting Hustlers")
        print(Hustler.objects.all().delete())

        print(f"Deleting Groups")
        print(Group.objects.filter(name__in=ALL_PERMISSION_GROUPS).delete())

        print(f"Deleting Users")
        print(User.objects.all().delete())
