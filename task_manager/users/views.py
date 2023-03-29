from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils.translation import gettext

from task_manager.users.models import User
from task_manager.users.forms import UserCreationForm, UserChangeForm, UserLoginForm

from task_manager.logger_config import logger


class UsersIndexView(View):

    def get(self, request, *args, **kwargs):
        page_name = gettext('Users')
        columns = [gettext('ID'), gettext('User Name'), gettext('Full name'), gettext('Date of creation')]
        users = User.objects.all()
        return render(request, 'users/index.html', context={
            'users': users,
            'page_name': page_name,
            'columns': columns,
        })
