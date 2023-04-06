from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext

from task_manager.users.forms import UserRegistrationForm
from task_manager.logger_config import logger


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')
    template_name = 'users/create.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, gettext('Вы успешно зарегистрировались!'))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, gettext('Ошибка регистрации!'))
        return response


class UserLoginView(LoginView):
    template_name = 'users/login.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, gettext('Ошибка входа!'))
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, gettext('Вы успешно вошли в систему!'))
        return response


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(self.request, gettext('Вы успешно вышли из системы!'))
        return response

    def get_next_page(self):
        return self.next_page


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'users/show.html'
    context_object_name = 'user'
    fields = ['username', 'first_name', 'last_name']


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name']
    template_name = 'users/update.html'

    def get_success_url(self):
        return reverse('user_update', kwargs={'pk': self.object.pk})

    def test_func(self):
        if not self.request.user.is_authenticated:
            logger.debug('User is not authenticated')
            self.raise_exception = False
            messages.error(self.request, gettext("Вы не авторизованы! Пожалуйста, выполните вход."))
            return False
        if self.request.user.pk != self.get_object().pk:
            logger.debug('User not match')
            self.raise_exception = False
            messages.error(self.request, gettext("У вас нет прав для изменения этого профиля."))
            return False
        return True

    def handle_no_permission(self):
        if not self.raise_exception:
            return redirect(self.request.META['HTTP_REFERER'])
        return super().handle_no_permission()

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, gettext('Информация обновлена!'))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, gettext('Ошибка обновления!'))
        return response


class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'

    def get_success_url(self):
        return reverse('user_delete', kwargs={'pk': self.object.pk})

    def test_func(self):
        if not self.request.user.is_authenticated:
            logger.debug('User is not authenticated')
            self.raise_exception = False
            messages.error(self.request, gettext("Вы не авторизованы! Пожалуйста, выполните вход."))
            return False
        if self.request.user.pk != self.get_object().pk:
            logger.debug('User not match')
            self.raise_exception = False
            messages.error(self.request, gettext("У вас нет прав для изменения этого профиля."))
            return False
        return True

    def handle_no_permission(self):
        if not self.raise_exception:
            return redirect(self.request.META['HTTP_REFERER'])
        return super().handle_no_permission()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, gettext('Пользователь удален!'))
        return super().delete(request, *args, **kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, gettext('Ошибка удаления!'))
