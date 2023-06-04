from django import forms
from django_filters import FilterSet, AllValuesFilter, Filter
from django_filters import ModelChoiceFilter, BooleanFilter, OrderingFilter
from .models import Task, Label, User, Status
from task_manager.logger_config import logger



class TaskFilter(FilterSet, AllValuesFilter):

    status = ModelChoiceFilter(field_name='status', queryset=Status.objects.all(), label='Status')
    executor = ModelChoiceFilter(field_name='executor', queryset=User.objects.all(), label='Executor')
    label = ModelChoiceFilter(field_name='label', queryset=Label.objects.all(), label='Label')
    my_tasks = BooleanFilter(label='Only my tasks', method='filter_my_task', field_name='my_tasks')


    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']

    def filter_my_task(self, queryset, value):
        if value:
            logger.error(f'User_current id={self.request.user.id}')
            return queryset.filter(executor=self.request.user)
        return queryset

