
from django.shortcuts import get_object_or_404, render
from .models import Repository, Issue,Milestone,Star

def get_milestones(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    milestones = Milestone.objects.filter(repo = repo)
    return render(request,"milestones.html",{"repository" : repo, "milestones": milestones})