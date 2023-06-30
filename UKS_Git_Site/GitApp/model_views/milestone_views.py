user_in_repositoryhref="{% url 'close_milestone' milestone_id=milestone.id %}"

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth.decorators import login_required
from django.urls import reverse


from GitApp.utils import milestone_progress,user_in_repository

from GitApp.models import *
from GitApp.forms import MilestoneForm
from GitApp.views import create_form_view

@login_required()
def create_milestone(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id, lead=request.user)
    milestone = Milestone(repository=repo, state=State.OPEN)
    return create_form_view(request, milestone, MilestoneForm, redirect('repo_milestones', repository_id=repository_id), "create_milestone.html")


def get_milestone(request,milestone_id):
    milestone = get_object_or_404(Milestone,id=milestone_id)
    issues = Milestone.objects.filter(milestone=milestone)
    progress = milestone_progress(milestone)
    show_edit = True
    # if user_in_repository(milestone.repository.id,request.user.id):
    #    show_edit = True 
    return render(request,"milestone.html",{"milestone":milestone,"progress":progress,"issues": issues , "show_edit": show_edit})

def get_milestones(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    milestones = Milestone.objects.filter(repository=repo)
    issues = Issue.objects.filter(repository=repo)
    return render(request, "milestones.html", {"repository": repo, "milestones": milestones, "issues": issues})
def milestone_open_issues(request,milestone_id):
    milestone = get_object_or_404(Milestone,id=milestone_id)
    issues = Issue.objects.filter(milestone=milestone,state=IssueState.OPEN)
    return render(request,"issues.html",{"issues":issues})

def milestone_closed_issues(request,milestone_id):
    milestone = get_object_or_404(Milestone,id=milestone_id)
    issues = Issue.objects.filter(milestone=milestone,state=IssueState.CLOSED)
    return render(request,"issues.html",{"issues":issues})

@login_required()
def close_milestone(request,milestone_id):
    milestone = get_object_or_404(Milestone,id=milestone_id)
    repository = get_object_or_404(Repository, id = milestone.repository.id)

    if not user_in_repository(repository.id,request.user.id):
        return HttpResponse("Error handler content", status=403)      
    
    milestone.state = State.CLOSED
    milestone.save()
    url = reverse("milestone_page", args=[milestone_id])
    return redirect(url)

@login_required()
def open_milestone(request,milestone_id):
    milestone = get_object_or_404(Milestone,id=milestone_id)
    repository = get_object_or_404(Repository, id = milestone.repository.id)

    if not user_in_repository(repository.id,request.user.id):
        return HttpResponse("Error handler content", status=403)
    milestone.state = State.OPEN
    milestone.save()
    url = reverse("milestone_page", args=[milestone_id])
    return redirect(url)

@login_required()
def update_milestone(request,milestone_id):
    milestone = get_object_or_404(Milestone,id=milestone_id)
    return create_form_view(request, milestone, MilestoneForm, redirect('milestone_page', milestone_id=milestone_id), "create_milestone.html")

@login_required
def delete_milestone(request,milestone_id):
    milestone = get_object_or_404(Milestone,id=milestone_id)
    if not user_in_repository(milestone.repository.id,request.user.id):
        return HttpResponse("Error handler content", status=403)   
    milestone.delete()
    url = reverse("single_repo", args=[milestone.repository.id])
    return redirect(url)