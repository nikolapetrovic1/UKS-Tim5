from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from GitApp.forms import CommentForm
from .models import Issue, Label, Repository, User, Star, Milestone, Comment, Reaction


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

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


def index(request):
    return render(request, "index_initial.html")


@cache_page(CACHE_TTL)
def cached_initial(request):
    redis.Redis(host="uks_tim5_redis", port=6379)
    repoNum = len(Repository.objects.all())
    return render(request, "cache_test.html", {"repoNum": repoNum})


def add_users_to_repo(request, repository_id, user_id):
    repo = get_object_or_404(Repository, id=repository_id)
    user = get_object_or_404(User, id=user_id)

    repo.developers = repo.developers + (",%s" % user)
    repo.save()

    return render(request, "add_users.html", {"repo": repo.developers, "user": user})


@login_required()
def add_users_to_repo(request, repository_id, user_id):
    owner = get_object_or_404(User, id=request.user.id)
    repo = get_object_or_404(Repository, id=repository_id, project_lead=owner)
    user = get_object_or_404(User, id=user_id)
    repo.developers.add(user)
    repo.save()

    return render(request, "add_users.html", {"repo": repo.developers, "user": user})


@login_required()
def new_star(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    user = get_object_or_404(User, id=request.user.id)
    star, _ = Star.objects.get_or_create(repository=repo, user=user)
    url = reverse("single_repository", args=[repository_id])
    return redirect(url)


@login_required()
def delete_star(request, star_id):
    star = get_object_or_404(Star, id=star_id)
    star.delete()

    user = get_object_or_404(User, id=request.user.id)

    template = loader.get_template("user_profile.html")

    context = {"user": user, "stars": user.stars.all()}

    return HttpResponse(template.render(context, request))


def get_labels(request):
    labels = Label.objects.all()
    return render(request, "labels.html", {"labels": labels})


def create_form_view(request, instance_object, FormType, redirect_page, template_name):
    if request.method == "POST":
        form = FormType(request.POST, instance=instance_object)
        if form.is_valid():
            form.save()
            return redirect_page
    else:
        form = FormType(instance=instance_object)
        return render(request, template_name, {"form": form})

    # ceated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # date_time = models.DateTimeField(auto_now=True)
    # content = models.TextField()
    # tas


def redirect_back(request):
    referer = request.META.get("HTTP_REFERER")

    if referer:
        return redirect(referer)
    else:
        # Redirect to a default page if there's no referer available
        return redirect("default_page_name")


@login_required()
def create_comment(request, task_id):
    if request.method == "POST":
        content = request.POST.get("content")
        comment = Comment(created_by=request.user, content=content, task_id=task_id)
        comment.save()

    referer = request.META.get("HTTP_REFERER")

    if referer:
        return redirect(referer)
    else:
        # Redirect to a default page if there's no referer available
        return redirect("default_page_name")


def get_reaction_types():
    return ["hand-thumbs-up", "hand-thumbs-down", "heart"]


def get_reaction_count(comment, user):
    counts = []
    for reaction in get_reaction_types():
        counts.append(
            [
                reaction,
                Reaction.objects.filter(comment=comment, code=reaction).count(),
                Reaction.objects.filter(
                    comment=comment, created_by=user, code=reaction
                ).exists()
                if user
                else False,
            ]
        )
    return counts


@login_required
def create_reaction(request, comment_id, reaction_type):
    if reaction_type not in get_reaction_types():
        return HttpResponseForbidden("Invalid reaction type")
    comment = get_object_or_404(Comment, id=comment_id)
    reaction = Reaction.objects.filter(
        created_by=request.user, code=reaction_type, comment=comment
    )
    if reaction:
        reaction.delete()
        return redirect_back(request)
    reaction = Reaction(created_by=request.user, code=reaction_type, comment=comment)
    reaction.save()
    return redirect_back(request)


# def create_form(request,FormClass,redirect_page,request_param):
#     if request.method == 'POST':
#         form = FormClass(request.POST,instance=request_param)
#         if form.is_valid():
#             form.save()
#             return redirect(redirect_page)
#     else:
#         form = FormClass(instance=request_param)
#         return render(request, template_name, {'form':form})
