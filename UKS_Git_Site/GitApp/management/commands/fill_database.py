from django.core.management.base import BaseCommand

from ...models import Repository, Star, User


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

        Star.objects.all().delete()

        star1 = Star(id=1, repository=r1)
        star1.save()

        star2 = Star(id=2, repository=r2)
        star2.save()

        User.objects.all().delete()

        user1 = User(id=1, firstName="Nikola", lastName="Stankovic", company="FTN", location="Novi Sad")
        user1.save()
        user1.stars.add(star1)
        user1.stars.add(star2)
        user1.save()

    def handle(self, *args, **options):
        self._add_repositories()