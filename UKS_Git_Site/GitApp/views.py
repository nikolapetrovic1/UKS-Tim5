from django.shortcuts import render, get_object_or_404
from .models import Repository, User

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
import redis
from django.template import loader


# Create your views here.
from django.http import HttpResponse

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def index(request):
    return render(request, "index_initial.html")


@cache_page(CACHE_TTL)
def cached_initial(request):
    redis.Redis(host='uks_tim5_redis', port=6379)
    repoNum = len(Repository.objects.all())
    return render(request, "cache_test.html", {"repoNum": repoNum})


def single_repo(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    return HttpResponse("You're looking at repository %s." % repo.name)

def profile_page(request, user_id):
    user = get_object_or_404(User, id=user_id)
    template = loader.get_template('profile_page.html')
    context = {'user': user, 'stars': user.stars.all()}
    return HttpResponse(template.render(context,request))