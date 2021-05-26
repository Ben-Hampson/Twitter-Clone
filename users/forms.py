from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class UserRegisterForm(
    UserCreationForm
):  # Adding an email field to our registration form
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # Affected model
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]  # Fields (+ their order) that we want in the form


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ["email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "image", "bio", "location", "website"]
        widgets = {"image": forms.FileInput}
