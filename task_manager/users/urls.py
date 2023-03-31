from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.UsersIndexView.as_view(), name='users_index'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout', views.UserLogoutView.as_view(), name='user_logout'),
    path('create/', views.UserFormCreateView.as_view(), name='user_create'),
    path('<int:id>/delete/', views.UserFormDeleteView.as_view(), name='user_delete'),
    path('<int:id>/edit/', views.UserFormCreateView.as_view, name='user_update'),
    path('<int:id>/', views.UserShowView.as_view(), name='user_show'),
]