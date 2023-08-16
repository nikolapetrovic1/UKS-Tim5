from GitApp.models import (
    Issue,
    Repository,
    Event,
    IssueCreated,
    Milestone,
    Label,
    Comment,
    Reaction,
)
from django.shortcuts import get_object_or_404, render, redirect
from GitApp.forms import IssueForm, CommentForm
from django.contrib.auth.decorators import login_required

from GitApp.views import get_reactions, get_user_reactions


def get_issue(request, repository_id, issue_id):
    repo = get_object_or_404(Repository, id=repository_id)
    issue = get_object_or_404(Issue, id=issue_id)
    issue_events = Event.objects.filter(entity_type="issue", entity_id=issue_id)
    comments = Comment.objects.filter(task=issue)
    all_user_reactions = []
    for comment in comments:
        user_reactions = Reaction.objects.filter(comment=comment)
        print(user_reactions, comment)
    return render(
        request,
        "issue.html",
        {
            "issue": issue,
            "repo": repo,
            "events": issue_events,
            "comments": comments,
            "reactions": all_user_reactions,
        },
    )


@login_required
def create_issue(request, repository_id):
    repository = get_object_or_404(Repository, id=repository_id)
    milestones = Milestone.objects.filter(repository=repository)
    labels = Label.objects.all()
    issue = Issue.objects.create(creator=request.user, repository=repository)
    if request.method == "POST":
        form = IssueForm(
            request.POST,
            queryset=repository.developers,
            milestones=milestones,
            labels=labels,
            instance=issue,
        )
        if form.is_valid():
            issue = form.save()
            issue_created = IssueCreated(
                created_by=request.user,
                entity_type="issue",
                entity_id=issue.id,
                title=issue.title,
            )
            issue_created.save()
            return redirect(
                "issue_page", repository_id=repository_id, issue_id=issue.id
            )
    else:
        form = IssueForm(
            queryset=repository.developers,
            milestones=milestones,
            labels=labels,
            instance=issue,
        )
        return render(request, "create_form.html", {"form": form})


@login_required
def update_issue(request, repository_id, issue_id):
    repository = get_object_or_404(Repository, id=repository_id)
    milestones = Milestone.objects.filter(repository=repository)
    labels = Label.objects.all()
    issue = get_object_or_404(Issue, repository=repository, id=issue_id)
    if request.method == "POST":
        form = IssueForm(
            request.POST,
            queryset=repository.developers,
            milestones=milestones,
            labels=labels,
            instance=issue,
        )
        if form.is_valid():
            issue = form.save()
            return redirect(
                "issue_page", repository_id=repository_id, issue_id=issue_id
            )
    else:
        form = IssueForm(
            queryset=repository.developers,
            milestones=milestones,
            labels=labels,
            instance=issue,
        )
        return render(request, "create_form.html", {"form": form})


@login_required
def close_issue(request, repository_id, issue_id):
    pass


@login_required
def open_issue(request, repository_id, issue_id):
    pass
