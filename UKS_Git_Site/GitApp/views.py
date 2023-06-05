from django.shortcuts import render, get_object_or_404
from .models import Repository, User, Star
from django.template.loader import render_to_string


from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

from django.contrib.auth.decorators import login_required, permission_required

import redis
from django.template import loader


# Create your views here.
from django.http import HttpResponse


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

def add_users_to_repo(request, repository_id, user_id):
    repo = get_object_or_404(Repository, id=repository_id)
    user = get_object_or_404(User, id=user_id)

    repo.contributors = repo.contributors + (",%s" % user)
    repo.save()

    return render(request,"add_users.html", {'repo' : repo.contributors, 'user' : user})

@login_required()
def new_star(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    user = get_object_or_404(User, id=request.user.id)
    star = Star(repository=repo)
    star.save()
    user.stars.add(star)
    user.save()
    template = loader.get_template('repository_page.html')
    context = {'repository': repo}
    return HttpResponse(template.render(context, request))
@login_required()
def delete_star(request, star_id):
    star = get_object_or_404(Star, id = star_id)
    star.delete()

    user = get_object_or_404(User, id=request.user.id)
    template = loader.get_template('user_profile.html')

    context = {'user': user, 'stars': user.stars.all()}

    return HttpResponse(template.render(context,request))

