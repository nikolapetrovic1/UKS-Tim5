from datetime import date
from django.shortcuts import get_object_or_404, render, redirect

from ..utils import milestone_progress

from ..views import create_form_view

from ..forms import IssueForm, RepositoryForm, RenameRepoForm
from ..models import Repository, Issue, Milestone, User, Label, IssueCreated
from django.contrib.auth.decorators import login_required
from copy import deepcopy


def rename_repo(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    create_form_view(
        request,
        repo,
        RenameRepoForm,
        redirect("single_repository", repository_id),
        "settings.html",
    )


@login_required()
def create_repository(request):
    lead = get_object_or_404(User, id=request.user.id)
    repo = Repository(lead=lead)
    return create_form_view(
        request, repo, RepositoryForm, redirect("index"), "create_milestone.html"
    )


def get_repo_issues(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    issues = Issue.objects.filter(repository=repo)
    return render(request, "issues.html", {"issues": issues})


def get_repos_by_user_id(request, user_id):
    user = get_object_or_404(User, id=user_id)
    repos = Repository.objects.filter(lead=user)
    return render(request, "repos.html", {"repos": repos})


@login_required()
def get_logged_user_repos(request):
    repos = Repository.objects.filter(lead=request.user)
    return render(request, "repos.html", {"repos": repos})


@login_required()
def fork_repo(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    forked_repo = deepcopy(repo)
    forked_repo.id = None
    forked_repo.save()
    forked_repo.forked_from = repo
    forked_repo.developers.clear()
    forked_repo.lead = request.user
    forked_repo.save()
    return redirect("single_repository", repository_id=forked_repo.id)


@login_required()
def watch_repo(request, repository_id):
    pass
