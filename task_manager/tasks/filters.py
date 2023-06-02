import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')
    status = django_filters.AllValuesFilter(field_name='status')
    executor = django_filters.AllValuesFilter(field_name='executor')
    label = django_filters.AllValuesFilter(field_name='label')
    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']
