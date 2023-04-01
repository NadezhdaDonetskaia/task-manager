from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils.translation import gettext

from task_manager.users.forms import UserRegistrationForm
from task_manager.logger_config import logger


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')
    template_name = 'users/create.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # authenticate user after registration
        user = authenticate(username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('password1'))
        login(self.request, user)
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
        messages.success(self.request, gettext('Вы успешно вошли!'))
        return response


class UserLogoutView(UserPassesTestMixin, LogoutView):
    next_page = reverse_lazy('home')

    def get_next_page(self):
        next_page = super().get_next_page()
        messages.success(self.request, gettext('Вы успешно вышли из системы!'))
        return next_page


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'users/show.html'
    context_object_name = 'user'
    fields = ['username', 'first_name', 'last_name']
    pk_url_kwarg = 'id'


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name']
    template_name = 'users/update.html'
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, gettext("У вас нет прав для изменения этого профиля."))
        return redirect('user_show')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, gettext('Информация обновлена!'))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, gettext('Ошибка обновления!'))
        return response

    def get_success_url(self):
        return reverse_lazy('user_show', kwargs={'id': self.object.id})


class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = User
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, gettext("У вас нет прав для удаления этого профиля."))
        return redirect('user_show')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, gettext('Пользователь удален!'))
        return super().delete(request, *args, **kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, gettext('Ошибка удаления!'))
        return response

    def get_success_url(self):
        return reverse_lazy('user_show', kwargs={'id': self.object.id})

