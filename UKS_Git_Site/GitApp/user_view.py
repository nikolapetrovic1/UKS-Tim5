from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

from django.core.exceptions import PermissionDenied
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash

from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import Field


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


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","email","username"]
        # label=_("Password"),
        # help_text=_(
        #     "Raw passwords are not stored, so there is no way to see this "
        #     "user's password, but you can change the password using "
        #     "<a href=\"{}\">this form</a>."
        # ),

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

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = "form-group"
        self.helper.form_class = "form-group"
        self.helper.form_action = "login"
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

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
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
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