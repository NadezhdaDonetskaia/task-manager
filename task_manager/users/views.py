from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext


from task_manager.users.forms import UserRegistrationForm
from task_manager.logger_config import logger



class UserView:
    model = User
    success_url = reverse_lazy('user_list')
    full_name = model.get_full_name
    model.full_name = full_name


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # logger.error(context)
        context['fields'] = ['id', 'username', 'full_name', 'date_joined']
        context['model_name'] = self.model._meta.verbose_name
        context['create_url'] = 'user_create'
        context['update_url'] = 'user_update'
        context['delete_url'] = 'user_delete'
        context['list_url'] = 'users_list'
        return context


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'create.html'

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
        messages.success(self.request, gettext('Вы успешно вошли в систему!'))
        return response


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(self.request, gettext('Вы успешно вышли из системы!'))
        return response



class UserListView(UserView, ListView):
    template_name = 'list.html'


class UserDetailView(UserView, DetailView):
    template_name = 'users/show.html'



class UserTestIdentification(UserView, UserPassesTestMixin):
    success_url = reverse_lazy('users_index')

    def test_func(self):
        text_err = ''
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
    

class UserUpdateView(LoginRequiredMixin, UserTestIdentification , UpdateView):
    template_name = 'update.html'
    


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, gettext('Пользователь успешно изменен'))
        return response



class UserDeleteView(LoginRequiredMixin, UserTestIdentification, DeleteView):
    template_name = 'delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, gettext('Пользователь успешно удален'))
        return super().delete(request, *args, **kwargs)
