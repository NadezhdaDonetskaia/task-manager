from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext

from task_manager.logger_config import logger

from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm


class StatusView:
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['id', 'name', 'created_at']
        context['fields_name'] = [
            'ID', 
            gettext('имя'),
            gettext('дата создания')
            ]
        context['model_name'] = self.model._meta.verbose_name
        context['create_url'] = 'status_create'
        context['update_url'] = 'status_update'
        context['delete_url'] = 'status_delete'
        context['list_url'] = 'statuses_list'
        return context

class StatusListView(StatusView, LoginRequiredMixin, ListView):
    template_name = 'list.html'

class StatusCreateView(StatusView, LoginRequiredMixin, CreateView):
    template_name = 'create.html'

    def form_valid(self, form):
        logger.debug('Form status create valid')
        form.instance.author = self.request.user
        return super().form_valid(form)


class StatusUpdateView(StatusView, LoginRequiredMixin, UpdateView):
    template_name = 'update.html'

    def form_valid(self, form):
        logger.debug('Form status update valid')
        messages.success(self.request, gettext('Статус успешно изменён'))
        return super().form_valid(form)


class StatusDeleteView(StatusView, LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'


    def delete(self, request, *args, **kwargs):
        logger.debug('Form status delete valid')
        messages.success(self.request, gettext('Статус успешно удален'))
        return super().delete(request, *args, **kwargs)
