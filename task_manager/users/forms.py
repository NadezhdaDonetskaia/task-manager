from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext
from task_manager.users.models import UserTask as User


class UserRegistrationForm(UserCreationForm):
    password2 = forms.CharField(
        label=gettext('Повторите пароль'),
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

