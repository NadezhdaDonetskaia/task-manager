from django import forms
from django_filters import FilterSet, AllValuesFilter
from django_filters import ModelChoiceFilter, BooleanFilter, ModelMultipleChoiceFilter
from django.utils.translation import gettext
from .models import Task, Label, User, Status
from task_manager.logger_config import logger


class TaskFilter(FilterSet, AllValuesFilter):

    status = ModelChoiceFilter(field_name='status', queryset=Status.objects.all(), label=gettext('Статус'))
    executor = ModelChoiceFilter(field_name='executor', queryset=User.objects.all(), label=gettext('Исполнитель'))
    labels = ModelMultipleChoiceFilter(field_name='labels', queryset=Label.objects.all(), label=gettext('Метка'))
    my_tasks = BooleanFilter(field_name='my_tasks', method='filter_my_tasks', label='Только свои задачи', widget=forms.CheckboxInput())

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_my_tasks(self, queryset, name, value):
        if value:
            logger.error(f'User_current id={self.request.user.id}')
            logger.error(queryset.filter(executor_id=self.request.user.id))
            return queryset.filter(author=self.request.user)
        return queryset
