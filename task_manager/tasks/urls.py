from django.urls import path

from task_manager.tasks import views

urlpatterns = [
    path('', views.TasksListView.as_view(), name='tasks_index'),
    # path('login/', views.UserLoginView.as_view(), name='user_login'),
    # path('logout', views.UserLogoutView.as_view(), name='user_logout'),
    # path('create/', views.UserRegistrationView.as_view(), name='user_create'),
    # path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    # path('<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_update'),
    # path('<int:pk>/', views.UserDetailView.as_view(), name='user_show'),
]