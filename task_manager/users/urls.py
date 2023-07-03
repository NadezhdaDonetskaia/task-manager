from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='users_list'),
    path('create/', views.UserRegistrationView.as_view(), name='user_create'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_show'),
]
