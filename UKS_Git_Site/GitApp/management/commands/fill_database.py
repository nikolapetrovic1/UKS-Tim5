from django.core.management.base import BaseCommand

from ...models import Repository
from ...models import CustomUser

class Command(BaseCommand):
    # args = '<args1 args2>'
    help = 'Komanda za popunjavanje baze sa inicijalnim vrednostima'

    def _add_repositories(self):
        Repository.objects.all().delete()

        r1 = Repository(id=1, name="Repo1")
        r1.save()

        r2 = Repository(id=2, name="Repo2")
        r2.save()

        r3 = Repository(id=3, name="Repo3")
        r3.save()
        
    def _add_users(self):
        CustomUser.objects.all().delete()

        CustomUser.objects.create_superuser("admin", "admin@mailinator.com", "admin")

        CustomUser.objects.create_user("user1", "user1@mailinator.com", "user1")
        CustomUser.objects.create_user("user2", "user2@mailinator.com", "user2")


    def handle(self, *args, **options):
        # self._add_repositories()
        self._add_users()
