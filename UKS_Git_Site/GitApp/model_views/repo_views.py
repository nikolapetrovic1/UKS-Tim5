from datetime import date
from random import betavariate
from django.shortcuts import get_object_or_404, render, redirect

from ..utils import milestone_progress, user_in_repository

from ..views import create_form_view

from ..forms import DefaultBranchForm, RepositoryForm, RenameRepoForm, CreateBranchForm
from ..models import (
    Branch,
    DefaultBranch,
    Repository,
    Issue,
    Milestone,
    User,
    Star,
)
from django.contrib.auth.decorators import login_required
from copy import deepcopy
from django.http import HttpResponse


def single_repo(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    default_branch = DefaultBranch.objects.filter(repository=repo).first()
    branches = Branch.objects.filter(repository=repo)
    star_count = Star.objects.filter(repository=repo).count()
    milestones = Milestone.objects.filter(repository=repo)
    issues = Issue.objects.filter(repository=repo)
    return render(
        request,
        "repository_page.html",
        {
            "repository": repo,
            "star_count": star_count,
            "issues": issues,
            "milestones": milestones,
            "labels": repo.labels.all(),
            "default_branch": default_branch,
            "branches": branches,
        },
    )


@login_required
def delete_repo(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id, lead=request.user)
    repo.delete()
    return redirect("index")


@login_required
def rename_repo(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    return create_form_view(
        request,
        repo,
        RenameRepoForm,
        redirect("single_repository", repository_id),
        "create_form.html",
    )


@login_required()
def create_repository(request):
    lead = get_object_or_404(User, id=request.user.id)
    repo = Repository(lead=lead)
    return create_form_view(
        request, repo, RepositoryForm, redirect("index"), "create_form.html"
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


@login_required
def create_branch(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    branch = Branch(repository=repo)
    if request.method == "POST":
        form = CreateBranchForm(
            request.POST,
            instance=branch,
        )
        if form.is_valid():
            if Branch.objects.filter(
                repository=repo, name=form.cleaned_data["name"]
            ).exists():
                return HttpResponse("Branch with same name already exists", status=403)
            form.save()
            return redirect("single_repository", repository_id=repository_id)
    else:
        form = CreateBranchForm(
            instance=branch,
        )
        return render(request, "create_form.html", {"form": form})


@login_required
def select_default_branch(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    default_branch = DefaultBranch.objects.filter(repository=repo).first()
    branches = Branch.objects.filter(repository=repo)
    if request.method == "POST":
        form = DefaultBranchForm(
            request.POST,
            branches=branches,
            instance=default_branch,
        )
        if form.is_valid():
            form.save()
            return redirect("single_repository", repository_id=repository_id)
    else:
        form = DefaultBranchForm(
            branches=branches,
            instance=default_branch,
        )
        return render(request, "create_form.html", {"form": form})
