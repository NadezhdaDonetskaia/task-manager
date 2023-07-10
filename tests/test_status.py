from django.urls import reverse_lazy
import pytest
from task_manager.logger_config import logger
from tests.conftest import Status


CREATE_URL = reverse_lazy('status_create')
UPDATE_URL = '/statuses/{id}/update/'
DELETE_URL = '/statuses/{id}/delete/'
INPUT_DATA = dict(name='status_test')
STATUS_NAME = 'New Status'
NEW_STATUS_NAME = 'Updated Status'


@pytest.mark.usefixtures('authorized_user')
@pytest.mark.django_db
def test_create_status(client):
    response = client.post(CREATE_URL, data={'name': 'New Status'})
    logger.debug(f'Resp status {response}')
    assert response.status_code == 302
    assert Status.objects.filter(name="New Status").exists()


@pytest.mark.django_db
def test_create_status_not_auth(client):
    response = client.post(CREATE_URL, data={'name': STATUS_NAME})
    assert response.url == '/login/'


@pytest.mark.usefixtures('authorized_user')
@pytest.mark.django_db
def test_update_status(client, status):
    url = UPDATE_URL.format(id=status.id)
    logger.error(f'status update url == {url}')
    client.post(url, data={'name': NEW_STATUS_NAME})
    updated_status = Status.objects.get(id=status.id)
    assert updated_status.name == NEW_STATUS_NAME


@pytest.mark.django_db
def test_update_status_not_auth(client, status):
    url = UPDATE_URL.format(id=status.id)
    logger.error(f'status update url == {url}')
    response = client.post(url, data={'name': NEW_STATUS_NAME})
    assert response.url == '/login/'


@pytest.mark.usefixtures('authorized_user')
@pytest.mark.django_db
def test_delete_status(client, status):
    url = DELETE_URL.format(id=status.id)
    client.post(url)
    assert not Status.objects.filter(id=status.id).exists()


@pytest.mark.django_db
def test_delete_status_not_auth(client, status):
    url = DELETE_URL.format(id=status.id)
    logger.debug(f'status delete url == {url}')
    response = client.post(url)
    assert response.url == '/login/'
    assert Status.objects.filter(id=status.id).exists()
