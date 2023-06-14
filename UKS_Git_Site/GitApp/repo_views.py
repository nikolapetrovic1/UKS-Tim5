
from django.shortcuts import get_object_or_404, render, redirect

from .views import create_form_view

from .forms import MilestoneForm, RepositoryForm
from .models import Repository, Issue,Milestone,Star, State, User

from django.contrib.auth.decorators import login_required

def get_milestones(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    milestones = Milestone.objects.filter(repo = repo)
    return render(request,"milestones.html",{"repository" : repo, "milestones": milestones})
@login_required()
def create_milestone(request,repository_id):
    repo = get_object_or_404(Repository, id=repository_id, lead = request.user)
    milestone = Milestone(repo=repo,state=State.OPEN)  
    return create_form_view(request,milestone,MilestoneForm,redirect('repo_milestones',repository_id=repository_id),"create_milestone.html")

@login_required()
def create_repository(request):
    lead = get_object_or_404(User,id=request.user.id)
    repo = Repository(lead=lead)
    return create_form_view(request,repo,RepositoryForm,redirect('index'),"create_milestone.html")

def get_repos_by_user(request,user_id):
    user = get_object_or_404(User,id = user_id)
    repos = Repository.objects.filter(lead=user)
    return render(request,"repos.html",{"repos":repos})
@login_required()
def get_logged_user_repos(request):
    repos = Repository.objects.filter(lead=request.user)
    return render(request,"repos.html",{"repos":repos})