from django.urls import reverse_lazy
import pytest
from task_manager.users.models import User
from task_manager.logger_config import logger
from tests.conftest import USER_PASSWORD


CREATE_URL = reverse_lazy('user_create')
UPDATE_URL = '/users/{id}/update/'
DELETE_URL = '/users/{id}/delete/'
USER_NAME = 'New User'
NEW_USER_NAME = 'Updated User'


@pytest.mark.django_db
def test_update_user_not_auth(client, user):
    url = UPDATE_URL.format(id=user.id)
    logger.error(f'user update url == {url}')
    response = client.post(url, data={'username': NEW_USER_NAME})
    assert response.url == '/login/'


@pytest.mark.usefixtures('authorized_user')
@pytest.mark.django_db
def test_delete_user(client, user):
    url = DELETE_URL.format(id=user.id)
    logger.debug(f'user delete url == {url}')
    client.post(url)
    assert not User.objects.filter(id=user.id).exists()


@pytest.mark.django_db
def test_delete_user_not_auth(client, user):
    url = DELETE_URL.format(id=user.id)
    logger.debug(f'user delete url == {url}')
    response = client.post(url)
    assert response.url == '/login/'
    assert User.objects.filter(id=user.id).exists()
