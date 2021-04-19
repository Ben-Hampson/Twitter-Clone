from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserRegisterForm(UserCreationForm):  # Adding an email field to our registration form
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # Affected model
        fields = ['username', 'email', 'password1', 'password2']  # Fields (+ their order) that we want in the form