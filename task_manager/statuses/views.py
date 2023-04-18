from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.utils.translation import gettext

from task_manager.logger_config import logger

from task_manager.statuses.models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'

    def handle_no_permission(self):
        logger.error('User do not auth')
        messages.error(self.request, gettext("Вы не авторизованы! Пожалуйста, выполните вход."))
        return redirect('user_login')


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = 'statuses/create.html'
    fields = ['name']
    success_url = reverse_lazy('statuses_list')

    def handle_no_permission(self):
        logger.error('User do not auth')
        messages.error(self.request, gettext("Вы не авторизованы! Пожалуйста, выполните вход."))
        return redirect('user_login')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    fields = ['name']
    success_url = reverse_lazy('statuses_list')

    def handle_no_permission(self):
        logger.error('User do not auth')
        messages.error(self.request, gettext("Вы не авторизованы! Пожалуйста, выполните вход."))
        return redirect('user_login')

    def form_valid(self, form):
        messages.success(self.request, gettext('Статус успешно изменён'))
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_list')

    def handle_no_permission(self):
        logger.error('User do not auth')
        messages.error(self.request, gettext("Вы не авторизованы! Пожалуйста, выполните вход."))
        return redirect('user_login')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, gettext('Статус успешно удален'))
        return super().delete(request, *args, **kwargs)
