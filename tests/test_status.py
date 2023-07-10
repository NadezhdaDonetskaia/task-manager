from django.urls import reverse_lazy
import pytest
from task_manager.logger_config import logger
from task_manager.logger_config import logger
from tests.conftest import Status

CREATE_URL = reverse_lazy('status_create')
UPDATE_URL = 'status/{id}/update/'
DELETE_URL = 'status/{id}/delete/'
INPUT_DATA = dict(name='status_test')


@pytest.mark.usefixtures('authorized_user')
@pytest.mark.django_db
def test_create_status(client):
    response = client.post(CREATE_URL, data={'name': 'New Status'})
    logger.debug(f'Resp status {response}')
    assert response.status_code == 302
    assert Status.objects.filter(name="New Status").exists()


@pytest.mark.usefixtures('authorized_user')
@pytest.mark.django_db
def test_update_status(client, status):
    url = UPDATE_URL.format(id=status.id)
    client.patch(url, data={'name': 'Updated Status'})
    assert status.name == 'Updated Status'


@pytest.mark.usefixtures('authorized_user')
@pytest.mark.django_db
def test_delete_status(client, status):
    url = DELETE_URL.format(id=status.id)
    client.delete(url)
    assert not Status.objects.filter(id=status.id).exists()



