from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.utils.translation import gettext

from task_manager.logger_config import logger

from task_manager.tasks.models import Task


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'

    def handle_no_permission(self):
        logger.error('User do not auth')
        messages.error(self.request, gettext("Вы не авторизованы! Пожалуйста, выполните вход."))
        return redirect('user_login')
