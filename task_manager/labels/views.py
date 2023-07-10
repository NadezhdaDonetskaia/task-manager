from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.utils.translation import gettext
from task_manager.logger_config import logger
from task_manager.users.views import UserLoginRequiredMixin
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm


class LabelListView(UserLoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(UserLoginRequiredMixin, CreateView):
    template_name = 'labels/create.html'
    form_class = LabelForm
    success_url = reverse_lazy('labels_list')

    def form_valid(self, form):
        logger.debug('Label status crete valid')
        messages.success(self.request, gettext('Метка успешно создана'))
        return super().form_valid(form)


class LabelUpdateView(UserLoginRequiredMixin, UpdateView):
    model = Label
    template_name = 'labels/update.html'
    form_class = LabelForm
    success_url = reverse_lazy('labels_list')

    def form_valid(self, form):
        logger.debug('Label status update valid')
        messages.success(self.request, gettext('Метка успешно изменена'))
        return super().form_valid(form)


class LabelDeleteView(UserLoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_list')

    def form_valid(self, form):
        try:
            delete = super().form_valid(form)
            messages.success(self.request, gettext('Метка успешно удалена'))
            return delete
        except ValidationError as err:
            messages.error(self.request, err.messages[0])
            return redirect('labels_list')
