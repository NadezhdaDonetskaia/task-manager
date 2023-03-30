from django.test import TestCase
from http import HTTPStatus

import pytest
from django.urls import reverse

from task_manager.users.models import User


def test_signup(client):
    """Test that a user can sign up."""
    response = client.get(reverse('users:signup'))
    assert response.status_code == HTTPStatus.OK

    with pytest.raises(User.DoesNotExist):
        User.objects.get(username='johndoe')

    response = client.post(reverse('users:signup'), data={
        'username': 'johndoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'password1': 'topsecret123',
        'password2': 'topsecret123',
    })
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('login')

    user = User.objects.get(username='johndoe')
    assert user.full_name() == 'John Doe'
    assert user.check_password('topsecret123')

