from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from ...models import *
from ...constants import create_default_labels


class Command(BaseCommand):
    # args = '<args1 args2>'
    help = "Komanda za popunjavanje baze sa inicijalnim vrednostima"

    def _add_data(self):
        User.objects.all().delete()

        content_type = ContentType.objects.get_for_model(User)
        # get_or_create koristimo za slucaj da postoji
        permission, _ = Permission.objects.get_or_create(
            codename="test_access",
            name="Test access",
            content_type=content_type,
        )
        # kreiranje grupe
        group, _ = Group.objects.get_or_create(name="test")

        group.permissions.add(permission)

        # kreiranje jos jednog korisnika koji nije u grupi, te nema permisije
        User.objects.create_superuser("admin", "admin@mailinator.com", "admin")

        user1 = User.objects.create_user(
            "user1", "user1@mailinator.com", "user1", company="FTN"
        )
        user1.groups.add(group)

        user2 = User.objects.create_user("user2", "user2@mailinator.com", "user2")

        Label.objects.all().delete()
        default_label = create_default_labels()
        for label in default_label:
            label.save()

        Repository.objects.all().delete()

        r1 = Repository(id=1, name="test", lead=user1)
        r1.save()
        r1.developers.add(user2)
        r1.labels.add(Label.objects.filter(id=1).first())
        r1.labels.add(Label.objects.filter(id=2).first())
        # r1.save()

        r2 = Repository(id=2, name="Repo2", lead=user2)
        r2.save()

        r3 = Repository(id=3, name="Repo3", lead=user1)
        r3.save()

        Milestone.objects.all().delete()
        milestone1 = Milestone(
            id=1,
            title="test milestone",
            description="test",
            due_date="2024-05-26",
            state=State.OPEN,
            repository=r1,
        )
        milestone1.save()

        Issue.objects.all().delete()
        issue1 = Issue(
            id=1,
            title="issue1",
            description="test",
            repository=r1,
            milestone=milestone1,
            creator=user1,
            state=IssueState.CLOSED,
        )
        issue2 = Issue(
            id=2,
            title="issue2",
            description="test",
            repository=r1,
            milestone=milestone1,
            creator=user1,
        )
        issue1.save()
        issue2.save()

        Comment.objects.all().delete()

        comm1 = Comment(id=1, created_by=user1, content="Great issue!!", task=issue1)
        comm1.save()

        Reaction.objects.all().delete()
        reaction1 = Reaction(id=1, created_by=user1, code="U+1F600", comment=comm1)
        reaction2 = Reaction(id=2, created_by=user1, code="U+1F44D", comment=comm1)
        reaction1.save()
        reaction2.save()
        IssueCreated.objects.all().delete()
        issue_created = IssueCreated(
            created_by=user1,
            entity_type="issue",
            entity_id=issue1.id,
            title=issue1.title,
        )
        issue_created.save()

        Star.objects.all().delete()

        star1 = Star(id=1, repository=r1, user=user1)
        star1.save()

        star2 = Star(id=2, repository=r2, user=user1)
        star2.save()

    def handle(self, *args, **options):
        self._add_data()
        # self._add_repositories(t)
