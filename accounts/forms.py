from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from polls.models import Type, Item, Review, Profile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

class EditAccountForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone","gender", "birth_date"]

class WriteReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "text"]
