from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import PermissionDenied

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


from .models import User, Star

from .forms import UserForm,UserLoginForm,UserUpdateForm

@login_required()
@permission_required('GitApp.test_access', raise_exception=True)
def test(request):
    return render(request,'user_profile.html')

@login_required()
def user_profile(request):
    user = get_object_or_404(User, id=request.user.id)
    stars = Star.objects.filter(user=user)
    return render(request,'user_profile.html',{"user": user,"stars":stars})

@login_required()
def delete_user(request):
    user = get_object_or_404(User, id=request.user.id)
    user.delete()
    return redirect('index')

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("index")
    else:
        form = UserLoginForm(request)
        return render(request,"login.html", {"form":form})
    
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    raise PermissionDenied()
       
def user_register(request,template_name='user_form.html'):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect('index')
    form = UserForm()
    return render(request,template_name,{'form':form})

login_required()
def user_update(request, template_name='user_form.html'):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserUpdateForm(instance=request.user)
        return render(request, template_name, {'form':form})

@login_required()
def user_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('user_profile')
        else:
            return redirect('change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'password_reset.html', {'form': form} )