import django_filters
from django_filters import rest_framework as filters
from .models import Task, Label, User, Status
from task_manager.logger_config import logger

class TaskFilter(django_filters.FilterSet):

    my_tasks = django_filters.BooleanFilter(label='Only my tasks', method='filter_my_task', field_name='my_tasks')
    status = django_filters.ModelChoiceFilter(field_name='status', queryset=Status.objects.all(), label='Status')
    executor = django_filters.ModelChoiceFilter(field_name='executor', queryset=User.objects.all(), label='Executor')
    label = django_filters.ModelChoiceFilter(field_name='label', queryset=Label.objects.all(), label='Label')
    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']

    def filter_my_task(self, queryset, name, value):
        if value:
            logger.error(f'User_current id={self.request.user.id}')
            return queryset.filter(executor=self.request.user)
        return queryset

