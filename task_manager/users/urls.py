from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='users_index'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout', views.UserLogoutView.as_view(), name='user_logout'),
    path('create/', views.UserRegistrationView.as_view(), name='user_create'),
    path('<int:id>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('<int:id>/edit/', views.UserUpdateView.as_view(), name='user_update'),
    path('<int:id>/', views.UserDetailView.as_view(), name='user_show'),
]