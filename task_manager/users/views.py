from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.translation import gettext
from django.contrib.auth.views import LogoutView

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
        form = UserEditForm(instance=user)
        title = user.username
        return render(request, f'users/show.html', context={
            'user': user,
            'title': title,
            'form': form,
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
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Welcome {username}')
                return redirect('home')
            else:
                messages.error(request, 'Неверные имя пользователя или пароль.')
        logger.debug('form user login is\'nt valid')
        messages.error(request, user_form.error_messages)
        return render(request, 'users/create.html', {
            'form': user_form,
            'title': title,
        })


class UserLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'You are logged out')
        return redirect('home')


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
            messages.info(request, f'User {user_form.cleaned_data["username"]} successfully registered')
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            return redirect('home')

        logger.error(user_form.errors)
        logger.debug(user_form.error_messages)
        errors = user_form.errors
        return render(request, 'users/create.html', {
            'form': user_form,
            'title': title,
            'errors': errors,
        })


class UserFormEditView(View):

    @login_required
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        form = UserEditForm(instance=user)
        return render(request, 'user_update', {'form': form, 'user': user})

    @login_required
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        form_change = UserEditForm(request.POST, instance=user)
        if form_change.is_valid():
            form_change.save()
            messages.success(request, 'Информация о пользователе была успешно обновлена')
            return redirect('home')

        return render(request, 'user_update', {'form': form_change, 'user': user})


class UserFormDeleteView(View):

    @login_required
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        form_delete = User
        return render(request, 'user_delete', {'user': user})

    @login_required
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if user:
            user.delete()
        return redirect('users')
