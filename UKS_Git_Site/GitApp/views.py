from django.shortcuts import render, get_object_or_404
from .models import Repository

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def single_repo(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    return HttpResponse("You're looking at repository %s." % repo.name)
