from django.urls import path

from task_manager.tasks import views

urlpatterns = [
    path('', views.TasksListView.as_view(), name='tasks_list'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
]
