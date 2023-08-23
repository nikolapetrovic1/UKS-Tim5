from datetime import date
from random import betavariate
from django.shortcuts import get_object_or_404, render, redirect
from copy import deepcopy
from ..utils import milestone_progress, user_in_repository

from ..views import create_form_view, get_reaction_count

from ..forms import (
    DefaultBranchForm,
    PullRequestForm,
    RepositoryForm,
    EditRepoForm,
    CreateBranchForm,
)
from ..models import (
    Branch,
    DefaultBranch,
    PullRequest,
    Repository,
    Issue,
    Milestone,
    User,
    Star,
    Comment,
    Commit,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def single_repo_branch(request, repository_id, branch_id):
    repo = get_object_or_404(Repository, id=repository_id)
    branch = Branch.objects.filter(id=branch_id, repository=repo).first()
    branches = Branch.objects.filter(repository=repo)
    star_count = Star.objects.filter(repository=repo).count()
    milestones = Milestone.objects.filter(repository=repo)
    issues = Issue.objects.filter(repository=repo)
    pull_requests = PullRequest.objects.filter(repository=repo)
    commits = Commit.objects.filter(repository=repo, branch=branch)
    starred = None
    if request.user.is_authenticated:
        starred = Star.objects.filter(repository=repo, user=request.user).first()
    return render(
        request,
        "repository_page.html",
        {
            "repository": repo,
            "star_count": star_count,
            "issues": issues,
            "milestones": milestones,
            "labels": repo.labels.all(),
            "current_branch": branch,
            "branches": branches,
            "pull_requests": pull_requests,
            "commits": commits,
            "starred": starred,
            "branch_id": branch_id,
        },
    )


def single_repo(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    default_branch = DefaultBranch.objects.filter(repository=repo).first()
    branches = Branch.objects.filter(repository=repo)
    star_count = Star.objects.filter(repository=repo).count()
    milestones = Milestone.objects.filter(repository=repo)
    issues = Issue.objects.filter(repository=repo)
    pull_requests = PullRequest.objects.filter(repository=repo)
    commits = Commit.objects.filter(repository=repo, branch=default_branch.branch)
    starred = None
    if request.user.is_authenticated:
        starred = Star.objects.filter(repository=repo, user=request.user).first()
    return render(
        request,
        "repository_page.html",
        {
            "repository": repo,
            "star_count": star_count,
            "issues": issues,
            "milestones": milestones,
            "labels": repo.labels.all(),
            "current_branch": default_branch,
            "branches": branches,
            "pull_requests": pull_requests,
            "commits": commits,
            "starred": starred,
            "branch_id": default_branch.branch.id,
        },
    )


@login_required
def delete_repo(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id, lead=request.user)
    repo.delete()
    return redirect("index")


@login_required
def edit_repo(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    developers = User.objects.exclude(pk=repo.lead.id)
    if request.method == "POST":
        form = EditRepoForm(request.POST, developers=developers, instance=repo)
        if form.is_valid():
            form.save()
        return redirect("single_repository", repository_id)
    else:
        form = EditRepoForm(developers=developers, instance=repo)
        return render(request, "create_form.html", {"form": form})


@login_required()
def create_repository(request):
    lead = get_object_or_404(User, id=request.user.id)
    repo = Repository(lead=lead)
    if request.method == "POST":
        form = RepositoryForm(request.POST, instance=repo)
        if form.is_valid():
            repo = form.save()
            branch = Branch(name="main", repository=repo)
            branch.save()
            default_branch = DefaultBranch(branch=branch, repository=repo)
            default_branch.save()
            return redirect("single_repository", repo.id)
    else:
        form = RepositoryForm(instance=repo)
        return render(request, "create_form.html", {"form": form})


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
    branches = Branch.objects.filter(repository=repo)
    if request.method == "POST":
        form = CreateBranchForm(
            request.POST,
            branches=branches,
            instance=branch,
        )
        if form.is_valid():
            if Branch.objects.filter(
                repository=repo, name=form.cleaned_data["name"]
            ).exists():
                return HttpResponse("Branch with same name already exists", status=403)
            target_branch = form.save()
            add_commits_from_branch(form.cleaned_data["from_branch"], target_branch)
            return redirect("single_repository", repository_id=repository_id)
    else:
        form = CreateBranchForm(
            branches=branches,
            instance=branch,
        )
        return render(request, "create_form.html", {"form": form})


def add_commits_from_branch(source_branch, target_branch):
    commits = Commit.objects.filter(branch=source_branch)
    for commit in commits:
        new_commit = deepcopy(commit)
        new_commit.id = None
        new_commit.branch = target_branch
        new_commit.save()


@login_required
def select_default_branch(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    default_branch = DefaultBranch.objects.filter(repository=repo).first()
    branches = Branch.objects.filter(repository=repo)
    print(branches)
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


@login_required
def create_pull_request(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    branches = Branch.objects.filter(repository=repo)
    pull_request = PullRequest(creator=request.user, repository=repo)
    milestones = Milestone.objects.filter(repository=repo)
    if request.method == "POST":
        form = PullRequestForm(
            request.POST,
            developers=repo.developers,
            milestones=milestones,
            branches=branches,
            instance=pull_request,
        )
        if form.is_valid():
            if form.cleaned_data["target"] == form.cleaned_data["source"]:
                return HttpResponse("Source different from target", status=403)
            form.save()
            return redirect("single_repository", repository_id=repository_id)
    else:
        form = PullRequestForm(
            developers=repo.developers,
            milestones=milestones,
            branches=branches,
            instance=pull_request,
        )
        return render(request, "create_form.html", {"form": form})


def get_pull_request(request, repository_id, pull_request_id):
    repo = get_object_or_404(Repository, id=repository_id)
    pull_request = get_object_or_404(PullRequest, repository=repo, id=pull_request_id)
    comments = Comment.objects.filter(task=pull_request)

    for comment in comments:
        if request.user.is_authenticated:
            comment.reactions = get_reaction_count(comment, request.user)
        else:
            comment.reactions = get_reaction_count(comment, None)
    return render(
        request,
        "pull_request.html",
        {"pull_request": pull_request, "comments": comments},
    )


def get_code_page(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    return render(
        request,
        "code_page.html",
        {},
    )
