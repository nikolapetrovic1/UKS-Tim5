from GitApp.models import Issue, Repository
from django.shortcuts import get_object_or_404, render, redirect


def get_issue(request, repository_id, issue_id):
    repo = get_object_or_404(Repository, id=repository_id)
    issue = get_object_or_404(Issue, id=issue_id)
    return render(
        request,
        "issue.html",
        {
            "issue": issue,
            "repo": repo,
        },
    )


def get_issue_history(issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
