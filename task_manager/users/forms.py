from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext


class UserRegistrationForm(UserCreationForm):


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    password = forms.CharField(required=True, widget=forms.PasswordInput)