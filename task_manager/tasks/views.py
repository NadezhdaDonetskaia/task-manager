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
from django_filters.rest_framework import DjangoFilterBackend


class TasksListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     my_tasks = self.request.GET.get(author_id=self.request.user.id)
    #     if my_tasks:
    #         queryset = queryset.filter(author_id=self.request.user.id)
    #     return queryset
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = self.get_filterset()  # Получить экземпляр TaskFilter
    #     return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/create.html'
    fields = ['name', 'executor', 'description', 'status', 'label']
    success_url = reverse_lazy('tasks_list')

    #
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/update.html'
    fields = ['name', 'description', 'status', 'executor', 'label']
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        messages.success(self.request, gettext('Статус успешно изменён'))
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_list')



    def delete(self, request, *args, **kwargs):
        messages.success(self.request, gettext('Статус успешно удален'))
        return super().delete(request, *args, **kwargs)
