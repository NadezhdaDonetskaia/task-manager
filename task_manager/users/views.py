from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils.translation import gettext

from task_manager.users.models import User
from task_manager.users.forms import UserAddForm, UserEditForm, UserLoginForm

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


class UserShowView(View):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs['id'])
        return render(request, 'user_show', context={
            'user': user,
        })


class UserLoginView(View):

    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        return render(request, 'user_login_in', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)



class UserFormCreateView(View):
    def get(self, request, *args, **kwargs):
        form = UserAddForm()
        return render(request, 'users/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        user_form = UserAddForm(request.POST)
        if user_form.is_valid():
            logger.debug(f'Form valid!!!')
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            return redirect('users/index.html')
        logger.debug(f'Form NOT valid!!!')
        return render(request, 'users/create.html', {'form': user_form})


class UserFormEditView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = UserEditForm(instance=user)
        return render(request, 'user_update', {'form': form, 'user_id': user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users_index')

        return render(request, 'user_update', {'form': form, 'user_id': user_id})


class UserFormDeleteView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        return render(request, 'user_delete', {'user_id': user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if user:
            user.delete()
        return redirect('users')