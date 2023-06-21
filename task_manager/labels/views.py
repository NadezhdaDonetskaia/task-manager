from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.utils.translation import gettext
from django.db.models.deletion import ProtectedError
from task_manager.logger_config import logger

from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm


class LabelView:
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = ['id', 'name', 'created_at']
        context['fields_name'] = [
            'ID', 
            gettext('имя'),
            gettext('дата создания')
            ]
        context['model_name'] = self.model._meta.verbose_name
        context['create_url'] = 'label_create'
        context['update_url'] = 'label_update'
        context['delete_url'] = 'label_delete'
        context['list_url'] = 'labels_list'
        return context


class LabelListView(LabelView, LoginRequiredMixin, ListView):
    template_name = 'list.html'


class LabelCreateView(LabelView, LoginRequiredMixin, CreateView):
    template_name = 'create.html'

    def form_valid(self, form):
        logger.debug('Label status crete valid')
        form.instance.author = self.request.user
        return super().form_valid(form)


class LabelUpdateView(LabelView, LoginRequiredMixin, UpdateView):
    template_name = 'update.html'

    def form_valid(self, form):
        logger.debug('Label status update valid')
        messages.success(self.request, gettext('Статус успешно изменён'))
        return super().form_valid(form)


class LabelDeleteView(LabelView, LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'


    def delete(self, request, *args, **kwargs):        
        logger.debug('Label status delete valid')
        try:
            messages.success(self.request, gettext('Статус успешно удален'))
            return super().delete(request, *args, **kwargs)
        except ProtectedError as err:
            messages.error(err.msg)
            return redirect('tasks_list')

