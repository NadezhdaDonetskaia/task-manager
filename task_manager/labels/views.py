from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.utils.translation import gettext
from django.db.models.deletion import ProtectedError
from task_manager.logger_config import logger

from task_manager.labels.models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    template_name = 'labels/create.html'
    fields = ['name']
    success_url = reverse_lazy('labels_list')

    def form_valid(self, form):
        logger.debug('Label status crete valid')
        form.instance.author = self.request.user
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    template_name = 'labels/update.html'
    fields = ['name']
    success_url = reverse_lazy('labels_list')

    def form_valid(self, form):
        logger.debug('Label status update valid')
        messages.success(self.request, gettext('Статус успешно изменён'))
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_list')


    def delete(self, request, *args, **kwargs):        
        logger.debug('Label status delete valid')
        ## НЕ РАБОТАЕТ -ВСЁ-РАВНО ВЫДАЁТ ОШИБКУ =(
        try:
            messages.success(self.request, gettext('Статус успешно удален'))
            return super().delete(request, *args, **kwargs)
        except ProtectedError as err:
            messages.error(err.msg)
            return redirect('tasks_list')

