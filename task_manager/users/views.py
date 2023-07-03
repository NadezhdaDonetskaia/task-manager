from django.contrib import messages

# from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext

from task_manager.users.models import User
from task_manager.users.forms import UserRegistrationForm, UserUpdateForm
from task_manager.logger_config import logger


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'users/create.html'

    def form_valid(self, form):
        logger.debug('Успешная регистрация')
        response = super().form_valid(form)
        messages.success(self.request, gettext('Пользователь успешно зарегистрирован'))
        return response

    def form_invalid(self, form):
        logger.error('Ошибка регистрации')
        response = super().form_invalid(form)
        messages.error(self.request, gettext('Ошибка регистрации!'))
        return response


class UserLoginView(LoginView):
    model = User
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        logger.error('Ошибка входа')
        response = super().form_invalid(form)
        messages.error(self.request,
                       gettext('Пожалуйста, введите правильные имя пользователя и пароль.\
                                Оба поля могут быть чувствительны к регистру.'))
        return response

    def form_valid(self, form):
        logger.debug("Успешный вход в систему")
        response = super().form_valid(form)
        messages.success(self.request, gettext('Вы залогинены'))
        return response


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(self.request, gettext('Вы разлогинены'))
        return response


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    fields = ['username', 'first_name', 'last_name']


class UserDetailView(DetailView):
    model = User
    template_name = 'users/show.html'
    context_object_name = 'user'
    fields = ['username', 'first_name', 'last_name']


class UserTestIdentification(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.pk != self.get_object().pk:
            logger.debug('User not match')
            self.raise_exception = False
            messages.error(self.request,
                           gettext('У вас нет прав для изменения другого пользователя.'))
            return False
        return True

    def handle_no_permission(self):
        if not self.raise_exception:
            return redirect(self.request.META['HTTP_REFERER'])
        return super().handle_no_permission()


class UserUpdateView(LoginRequiredMixin, UserTestIdentification, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('users_list')
    template_name = 'users/update.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, gettext('Пользователь успешно изменен'))
        return response


class UserDeleteView(LoginRequiredMixin, UserTestIdentification, DeleteView):
    model = User
    success_url = reverse_lazy('users_list')
    template_name = 'users/delete.html'

    def form_valid(self, form):
        messages.success(self.request, gettext('Пользователь успешно удален'))
        return super().form_valid(form)
