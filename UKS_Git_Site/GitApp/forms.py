from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import Field

from .models import User

class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = "form-group"
        self.helper.form_class = "form-group"
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Register'))
    class Meta:
        model = User
        fields = ["first_name","last_name","email","username"]

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = "form-group"
        self.helper.form_class = "form-group"
        self.helper.form_action = "login"
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

class UserUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = "form-group"
        self.helper.form_class = "form-group"
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = User
        fields = ["first_name","last_name","email","username"]