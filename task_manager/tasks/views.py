from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.utils.translation import gettext

from django_filters.views import FilterView

from task_manager.logger_config import logger

from task_manager.tasks.models import Task
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from django_filters.rest_framework import DjangoFilterBackend




class TasksListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter


class TaskCreateView(LoginRequiredMixin, CreateView):
    template_name = 'tasks/create.html'
    form_class = StatusForm = TaskForm
    success_url = reverse_lazy('tasks_list')

    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, gettext('Задача успешно создана'))
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/update.html'
    form_class = StatusForm = TaskForm
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        messages.success(self.request, gettext('Задача успешно изменена'))
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_list')


    def form_valid(self, form):
        messages.success(self.request, gettext('Задача успешно удалена'))
        return super().form_valid(form)
