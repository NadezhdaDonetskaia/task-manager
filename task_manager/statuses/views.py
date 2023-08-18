from django.contrib import messages
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext
from django.shortcuts import redirect

from task_manager.logger_config import logger
from task_manager.users.views import UserLoginRequiredMixin
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm


class StatusListView(UserLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class StatusCreateView(UserLoginRequiredMixin, CreateView):
    template_name = 'statuses/create.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        logger.debug('Form status create valid')
        messages.success(self.request, gettext('Status added successfully'))
        return super().form_valid(form)


class StatusUpdateView(UserLoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        logger.debug('Form status update valid')
        messages.success(self.request, gettext('Status changed successfully'))
        return super().form_valid(form)


class StatusDeleteView(UserLoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        try:
            delete = super().form_valid(form)
            messages.success(self.request, gettext('Status deleted successfully'))
            return delete
        except ProtectedError:
            messages.error(self.request,
                           gettext("Can't delete status because it's in use"))
            return redirect('statuses_list')
