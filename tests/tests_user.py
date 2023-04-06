import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import RequestFactory
from mixer.backend.django import mixer
from myapp.views import UserRegistrationView, UserUpdateView, UserDeleteView

pytestmark = pytest.mark.django_db


class TestUserRegistrationView:
    def test_get(self, client):
        url = reverse('user_registration')
        response = client.get(url)
        assert response.status_code == 200
        assert 'users/registration.html' in [template.name for template in response.templates]

    def test_post_success(self, client):
        url = reverse('user_registration')
        data = {'username': 'testuser', 'password1': 'testpass123', 'password2': 'testpass123'}
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('login')

    def test_post_failure(self, client):
        url = reverse('user_registration')
        data = {'username': 'testuser', 'password1': 'testpass123', 'password2': 'testpass'}
        response = client.post(url, data)
        assert response.status_code == 200
        assert 'users/registration.html' in [template.name for template in response.templates]


class TestUserUpdateView:
    def test_get(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        url = reverse('user_update', kwargs={'id': user.id})
        response = client.get(url)
        assert response.status_code == 200
        assert 'users/update.html' in [template.name for template in response.templates]

    def test_post_success(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        url = reverse('user_update', kwargs={'id': user.id})
        data = {'username': 'testuser2', 'first_name': 'Test', 'last_name': 'User'}
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('user_show', kwargs={'id': user.id})

    def test_post_failure(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        url = reverse('user_update', kwargs={'id': user.id})
        data = {'username': '', 'first_name': 'Test', 'last_name': 'User'}
        response = client.post(url, data)
        assert response.status_code == 200
        assert 'users/update.html' in [template.name for template in response.templates]


class TestUserDeleteView:
    def test_get(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        url = reverse('user_delete', kwargs={'id': user.id})
        response = client.get(url)
        assert response.status_code == 200
        assert 'users/delete.html' in [template.name for template in response.templates]

    def test_post_success(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        url = reverse('user_delete', kwargs={'id': user.id})
        response = client.post(url)
        assert response.status_code == 302
        assert response.url == reverse('index')

    def test_post_failure(self, client):
        user = mixer.blend(User)
        another_user = mixer.blend(User)
        client.force_login(another_user)
        url = reverse('user_delete', kwargs