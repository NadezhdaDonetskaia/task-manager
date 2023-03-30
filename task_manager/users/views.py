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
        title = 'Login'
        form = UserLoginForm()
        return render(request, 'users/login.html', {
            'form': form,
            'title': title,
        })

    def post(self, request, *args, **kwargs):
        title = 'Login'
        user_form = UserLoginForm(request.POST)
        if user_form.is_valid():
            logger.debug(f'Form login is valid')
            user_name = user_form.username
            message_success = f'Welcome {user_name}'
            return redirect('index.html', {
                'message_success': message_success,
            })
        logger.error(user_form.errors)
        logger.debug('form user login is\'valid')
        errors = user_form.errors
        message = 'Please enter the correct username and password. Both fields can be case sensitive.'
        return render(request, 'users/create.html', {
            'form': user_form,
            'title': title,
            'errors': errors,
            'message': message
        })




class UserFormCreateView(View):
    def get(self, request, *args, **kwargs):
        title = 'Registration'
        form = UserAddForm()
        return render(request, 'users/create.html', {
            'form': form,
            'title': title,
        })

    def post(self, request, *args, **kwargs):
        title = 'Registration'
        user_form = UserAddForm(request.POST)
        if user_form.is_valid():
            logger.debug(f'Form user create is valid')
            new_user = user_form.save(commit=False)
            message = f'User {user_form.cleaned_data["username"]} successfully registered'
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            return redirect('home', {
                'user': new_user,
                'message_success': message,
            })

        logger.error(user_form.errors)
        logger.debug(user_form.error_messages)
        errors = user_form.errors
        return render(request, 'users/create.html', {
            'form': user_form,
            'title': title,
            'errors': errors,
        })


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