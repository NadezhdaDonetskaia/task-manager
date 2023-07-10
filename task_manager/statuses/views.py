from django.contrib import messages
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext
from django.shortcuts import redirect

from task_manager.logger_config import logger

from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, CreateView):
    template_name = 'statuses/create.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        logger.debug('Form status create valid')
        messages.success(self.request, gettext('Статус успешно создан'))
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        logger.debug('Form status update valid')
        messages.success(self.request, gettext('Статус успешно изменен'))
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        try:
            delete = super().form_valid(form)
            messages.success(self.request, gettext('Статус успешно удален'))    
            return delete  
        except ProtectedError as err:
            messages.error(self.request, gettext('Невозможно удалить статус, потому что он используется'))
            return redirect('statuses_list')
