from django.core.management.base import BaseCommand

from ...models import Repository
from ...models import User

class Command(BaseCommand):
    # args = '<args1 args2>'
    help = 'Komanda za popunjavanje baze sa inicijalnim vrednostima'

    def _add_repositories(self):
        Repository.objects.all().delete()

        r1 = Repository(id=1, name="Repo1",contributors="User1")
        r1.save()

        r2 = Repository(id=2, name="Repo2",contributors="User2")
        r2.save()

        r3 = Repository(id=3, name="Repo3",contributors="User3")
        r3.save()
        
    def _add_users(self):
        User.objects.all().delete()
        
        u1 = User(id=1,name="User1")
        u1.save()
        
        u2 = User(id=2,name="User2")
        u2.save()
        
        u3 = User(id=3,name="User3")
        u3.save()
    
    def handle(self, *args, **options):
        self._add_repositories()
        self._add_users()
