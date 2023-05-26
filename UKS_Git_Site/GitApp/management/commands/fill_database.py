from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from ...models import User, Project, Milestone, Repository, State
import datetime
class Command(BaseCommand):
    # args = '<args1 args2>'
    help = 'Komanda za popunjavanje baze sa inicijalnim vrednostima'

    def _add_repositories(self):
        Repository.objects.all().delete()

        r1 = Repository(id=1, name="Repo1", contributors="User1")
        r1.save()

        r2 = Repository(id=2, name="Repo2", contributors="User1")
        r2.save()

        r3 = Repository(id=3, name="Repo3", contributors="User1")
        r3.save()
        
    def _add_users(self):
        User.objects.all().delete()
        content_type = ContentType.objects.get_for_model(User)
        # get_or_create koristimo za slucaj da postoji
        permission, _ = Permission.objects.get_or_create(
            codename='test_access',
            name='Test access',
            content_type=content_type,
        )
        # kreiranje grupe
        group, _ = Group.objects.get_or_create(name="test")

        group.permissions.add(permission)
        
        # kreiranje jos jednog korisnika koji nije u grupi, te nema permisije
        User.objects.create_superuser("admin", "admin@mailinator.com", "admin")

        user1 = User.objects.create_user("user1", "user1@mailinator.com", "user1")
        user1.groups.add(group)
        # user1.user_permissions.add(permission)
        User.objects.create_user("user2", "user2@mailinator.com", "user2")

    def _add_data(self):
        Project.objects.all().delete()
        project1 = Project(title="test")
        project1.save()
        Milestone.objects.all().delete()
        milestone1 = Milestone(title="test milestone",description="test",due_date = '2024-05-26',state=State.OPEN,project= project1)
        milestone1.save()

    def handle(self, *args, **options):
        self._add_data()
        self._add_repositories()
        self._add_users()
