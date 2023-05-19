from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

from django.core.exceptions import PermissionDenied
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User     
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'roll': forms.NumberInput(attrs={'class': 'form-control'}),
        # }
        fields = ["first_name","last_name","email","username"]

	# def save(self, commit=True):
	# 	user = super(NewUserForm, self).save(commit=False)
	# 	user.email = self.cleaned_data['email']
	# 	if commit:
	# 		user.save()
	# 	return user


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","email","username"]

@login_required()
@permission_required('GitApp.test_access', raise_exception=True)
def test(request):
    return render(request,'user_profile.html')

@login_required()
def user_profile(request):
    user = get_object_or_404(User, id=request.user.id)
    form = UserUpdateForm(request.POST or None, instance=user) 
    return render(request,'user_profile.html',{"object": user,"form": form})

@login_required()
def delete_user(request):
    user = get_object_or_404(User, id=request.user.id)
    user.delete()
    return redirect('index')

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


       
def user_register(request,template_name='user_form.html'):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request,template_name,{'form':form})

login_required()
def user_update(request, template_name='user_form.html'):
    user = get_object_or_404(User, pk=request.user.id)
    form = UserUpdateForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('user_profile')
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
        args = {'form': form}
        return render(request, 'password_reset.html', args) 