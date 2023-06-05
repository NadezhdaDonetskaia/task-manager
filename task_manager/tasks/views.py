from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import redirect
from django.utils.translation import gettext

from django_filters.views import FilterView

from task_manager.logger_config import logger

from task_manager.tasks.models import Task
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from django_filters.rest_framework import DjangoFilterBackend


class TaskView(View):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['id', 'name', 'status', 'author', 'executor', 'created_at']
        context['model_name'] = self.model._meta.verbose_name
        context['create_url'] = 'task_create'
        context['update_url'] = 'task_update'
        context['delete_url'] = 'task_delete'
        context['list_url'] = 'tasks_list'
        return context


class TasksListView(TaskView, LoginRequiredMixin, FilterView):
    template_name = 'list.html'
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter


class TaskCreateView(TaskView, LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    success_url = reverse_lazy('tasks_list')

    #
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(TaskView, LoginRequiredMixin, UpdateView):
    template_name = 'update.html'

    def form_valid(self, form):
        messages.success(self.request, gettext('Статус успешно изменён'))
        return super().form_valid(form)


class TaskDeleteView(TaskView, LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'



    def delete(self, request, *args, **kwargs):
        messages.success(self.request, gettext('Статус успешно удален'))
        return super().delete(request, *args, **kwargs)
