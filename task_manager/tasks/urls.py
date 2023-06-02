from django.urls import path
from django_filters.views import FilterView

from task_manager.tasks import views
from task_manager.tasks.models import Task

urlpatterns = [
    # path("list/", FilterView.as_view(model=Task), name="product-list"),
    path('', views.TasksListView.as_view(), name='tasks_list'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
]
