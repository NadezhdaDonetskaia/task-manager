from django.contrib.auth import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from task_manager.users.models import User


class UserLoginForm(forms.AuthenticationForm):
    username = User.username
    password = User.password
    field = ['username', 'password']


class UserAddForm(forms.UserCreationForm):
    class Meta:
        model = User
        model.username.help_text = 'Только буквы, цифры и символы @/./+/-/_.'
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')


class UserEditForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'password')