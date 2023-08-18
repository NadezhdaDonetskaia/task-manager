from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from django_filters.views import FilterView
from django_filters.rest_framework import DjangoFilterBackend

from task_manager.logger_config import logger

from task_manager.tasks.models import Task
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.views import UserLoginRequiredMixin


class TasksListView(UserLoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter


class TaskDetailView(UserLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show.html'
    context_object_name = 'task'


class TaskCreateView(UserLoginRequiredMixin, CreateView):
    template_name = 'tasks/create.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        logger.debug('Задача успешно создана')
        messages.success(self.request, gettext('Task added successfully'))
        return super().form_valid(form)


class TaskUpdateView(UserLoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/update.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        messages.success(self.request, gettext('Task changed successfully'))
        return super().form_valid(form)


class TaskDeleteView(UserLoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        task = self.get_object()
        if self.request.user.pk != task.author.pk:
            messages.error(self.request, gettext('A task can only be deleted by its author'))
            return redirect('tasks_list')
        try:
            delete = super().form_valid(form)
            messages.success(self.request, gettext('Task deleted successfully'))
            return delete
        except ValidationError as err:
            messages.error(self.request, err.messages[0])
            return redirect('tasks_list')
