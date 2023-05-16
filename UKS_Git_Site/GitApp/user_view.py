from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .models import User



@login_required()
@permission_required('GitApp.test_access', raise_exception=True)
def test(request):
    return render(request,'user_profile.html')

@login_required()
def user_profile(request):
    user = get_object_or_404(User, id=request.user.id)
    return render(request,'user_profile.html',{"object": user})

@login_required()
def delete_user(request):
    user = get_object_or_404(User, id=request.user.id)
    user.delete()
    return redirect('index')
# @login_required()
    
# class UserUpdate(UpdateView):
#     model = User
#     fields = ['name', 'pages']
#     success_url = reverse_lazy('book_list')

def user_login(request):
    if request.method == 'GET':
        return render(request, "login.html")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request,user)
            return redirect("user_profile")
        else:
            return redirect('login')
    else:
        return redirect('index')

    
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    raise PermissionDenied()