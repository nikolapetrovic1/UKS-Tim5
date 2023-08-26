from copy import deepcopy
from datetime import date
from random import betavariate

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import (
    CreateBranchForm,
    DefaultBranchForm,
    EditRepoForm,
    PullRequestForm,
    RepositoryForm,
)
from ..models import (
    Branch,
    Comment,
    Commit,
    DefaultBranch,
    Issue,
    Milestone,
    PullRequest,
    Repository,
    RepositoryState,
    Star,
    State,
    User,
    Watch,
)
from ..views import create_form_view, get_reaction_count, redirect_back


def single_repo_branch(request, repository_id, branch_id):
    repo = get_object_or_404(Repository, id=repository_id)
    if (repo.private == RepositoryState.PRIVATE) and (
        request.user not in repo.developers.all()
    ):
        raise Http404("Resource not found")
    branch = Branch.objects.get(id=branch_id, repository=repo)
    branches = Branch.objects.filter(repository=repo)
    star_count = Star.objects.filter(repository=repo).count()
    milestones = Milestone.objects.filter(repository=repo)
    issues = Issue.objects.filter(repository=repo)
    pull_requests = PullRequest.objects.filter(repository=repo)
    commits = Commit.objects.filter(branch=branch)
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
    if (repo.private == RepositoryState.PRIVATE) and (
        request.user not in repo.developers.all()
    ):
        raise Http404("Resource not found")
    default_branch = DefaultBranch.objects.get(repository=repo)
    branches = Branch.objects.filter(repository=repo)
    star_count = Star.objects.filter(repository=repo).count()
    milestones = Milestone.objects.filter(repository=repo)
    issues = Issue.objects.filter(repository=repo)
    pull_requests = PullRequest.objects.filter(repository=repo)
    commits = Commit.objects.filter(branch=default_branch.branch)
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
    repo = get_object_or_404(Repository, id=repository_id, lead=request.user)
    developers = User.objects.exclude(pk=repo.lead.id)
    if request.method == "POST":
        form = EditRepoForm(request.POST, developers=developers, instance=repo)
        if form.is_valid():
            form.save()
        return redirect("single_repository", repository_id)
    else:
        form = EditRepoForm(developers=developers, instance=repo)
    return render(request, "create_form.html", {"form": form})


@login_required
def create_repository(request):
    repo = Repository(lead=request.user)
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
    branch = Branch.objects.get(name="main", repository=repo)
    commits = Commit.objects.filter(branch=branch)
    branch.id = None
    branch.repository = forked_repo
    branch.save()
    for commit in commits:
        commit.id = None
        commit.branch = branch
        commit.save()
    default_branch = DefaultBranch(branch=branch, repository=forked_repo)
    default_branch.save()
    return redirect("single_repository", repository_id=forked_repo.id)


@login_required()
def watch_repo(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    if (repo.private == RepositoryState.PRIVATE) and (
        request.user not in repo.developers.all()
    ):
        raise Http404("Resource not found")
    Watch.objects.get_or_create(repository=repo, user=request.user)
    return redirect("watched_repos")


@login_required
def get_watched_repos(request):
    watched = Watch.objects.filter(user=request.user).prefetch_related("repository")
    for watch in watched:
        branches = Branch.objects.filter(repository=watch.repository)
        watch.repository.branches = branches
        for branch in branches:
            branch.commits = Commit.objects.filter(branch=branch)
    return render(request, "watched_repos.html", {"watched": watched})


@login_required()
def unwatch_repo(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    watch = Watch.objects.get(repository=repo, user=request.user)
    watch.delete()
    return redirect("watched_repos")


@login_required
def create_branch(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    if not request.user in repo.developers.all():
        return HttpResponseForbidden("No access")
    branch = Branch(repository=repo)
    branches = Branch.objects.filter(repository=repo)
    if request.method == "POST":
        form = CreateBranchForm(
            request.POST,
            branches=branches,
            instance=branch,
        )
        if form.is_valid():
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
    repo = get_object_or_404(Repository, id=repository_id, lead=request.user)
    default_branch = DefaultBranch.objects.get(repository=repo)
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
    source_commits, target_commits = get_pr_commits(repository_id, pull_request_id)
    diff = list(set(source_commits) - set(target_commits))
    comments = Comment.objects.filter(task=pull_request)
    for comment in comments:
        if request.user.is_authenticated:
            comment.reactions = get_reaction_count(comment, request.user)
        else:
            comment.reactions = get_reaction_count(comment, None)
    return render(
        request,
        "pull_request.html",
        {
            "pull_request": pull_request,
            "comments": comments,
            "source_commits": source_commits,
            "target_commits": target_commits,
            "diff": diff,
            "can_merge": can_merge_pr(pull_request),
        },
    )


def can_merge_pr(pull_request):
    target_commits = Commit.objects.filter(branch=pull_request.target)
    source_commits = Commit.objects.filter(branch=pull_request.source)
    last_target_commit = target_commits.last()
    if not target_commits:
        return True, source_commits
    for i, commit in enumerate(source_commits):
        if commit.hash == last_target_commit.hash:
            return True, source_commits[i + 1 :]
    return False, []


@login_required
def merge_pr(request, repository_id, pull_request_id):
    repo = get_object_or_404(Repository, id=repository_id)
    if not request.user in repo.developers.all():
        return HttpResponseForbidden("No access")
    pull_request = get_object_or_404(PullRequest, repository=repo, id=pull_request_id)
    can_merge, commits_to_add = can_merge_pr(pull_request)
    if not can_merge:
        return HttpResponse("Not able to merge", status=403)
    for commit in commits_to_add:
        commit.id = None
        commit.branch = pull_request.target
        commit.save()
    pull_request.state = State.MERGED
    pull_request.save()
    return redirect("single_repository", repository_id=repository_id)


@login_required
def close_pr(request, repository_id, pull_request_id):
    repo = get_object_or_404(Repository, id=repository_id)
    if not request.user in repo.developers.all():
        return HttpResponseForbidden("No access")
    pull_request = get_object_or_404(PullRequest, repository=repo, id=pull_request_id)
    pull_request.state = State.CLOSED
    pull_request.save()

    return redirect("single_repository", repository_id=repository_id)


def get_pr_commits(repository_id, pull_request_id):
    repo = get_object_or_404(Repository, id=repository_id)
    pull_request = get_object_or_404(PullRequest, repository=repo, id=pull_request_id)
    target_commits = Commit.objects.filter(branch=pull_request.target)
    source_commits = Commit.objects.filter(branch=pull_request.source)
    return target_commits, source_commits


def get_code_page(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    return render(
        request,
        "code_page.html",
        {},
    )
