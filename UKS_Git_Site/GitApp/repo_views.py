
from datetime import date
from django.shortcuts import get_object_or_404, render, redirect

from .utils import milestone_progress

from .views import create_form_view

from .forms import IssueForm, MilestoneForm, RepositoryForm, RenameRepoForm
from .models import Repository, Issue, Milestone, Star, State, User, Label

from django.contrib.auth.decorators import login_required



def rename_repo(request,repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    create_form_view(request,repo,RenameRepoForm,redirect('single_repository', repository_id),"settings.html")




@login_required()
def create_repository(request):
    lead = get_object_or_404(User, id=request.user.id)
    repo = Repository(lead=lead)
    return create_form_view(request, repo, RepositoryForm, redirect('index'), "create_milestone.html")


@login_required()
def create_issue(request, repository_id):
    repository = get_object_or_404(Repository, id=repository_id)
    milestones = Milestone.objects.filter(repository=repository)
    labels = Label.objects.all()
    issue = Issue.objects.create(creator=request.user, repository=repository)
    if request.method == 'POST':
        form = IssueForm(request.POST, queryset=repository.developers,
                         milestones=milestones, labels=labels, instance=issue)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = IssueForm(queryset=repository.developers,
                         milestones=milestones, labels=labels,instance=issue)
        return render(request, "create_milestone.html", {'form': form})


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
