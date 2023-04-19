from django.core.management.base import BaseCommand

from ...models import Repository


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

    def handle(self, *args, **options):
        self._add_repositories()
