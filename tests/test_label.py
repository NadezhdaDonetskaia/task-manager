from django.urls import reverse_lazy
import pytest
from task_manager.logger_config import logger
from tests.conftest import Label

CREATE_URL = reverse_lazy('label_create')
UPDATE_URL = '/labels//{id}/update'
DELETE_URL = '/labels//{id}/delete'
LABEL_NAME = 'New Label'
NEW_LABEL_NAME = 'Updated Label'

@pytest.mark.usefixtures('authorized_user')
@pytest.mark.django_db
def test_create_label(client):
    response = client.post(CREATE_URL, data={'name': LABEL_NAME})
    logger.error(f'Resp label {Label.objects.get(name=LABEL_NAME)}')
    assert response.status_code == 302
    assert Label.objects.filter(name="New Label").exists()


@pytest.mark.django_db
def test_create_label_not_auth(client):
    response = client.post(CREATE_URL, data={'name': LABEL_NAME})
    assert response.url == '/login/'
    assert not Label.objects.filter(name="New Label").exists()


@pytest.mark.usefixtures('authorized_user')
@pytest.mark.django_db
def test_update_label(client, label):
    url = UPDATE_URL.format(id=label.id)
    logger.error(f'label update url == {url}')
    client.post(url, data={'name': NEW_LABEL_NAME})
    # client.post('/labels/1/update', data={'name': NEW_LABEL_NAME})
    updated_label = Label.objects.get(id=label.id)
    assert updated_label.name == NEW_LABEL_NAME


@pytest.mark.django_db
def test_update_label(client, label):
    url = UPDATE_URL.format(id=label.id)
    logger.error(f'label update url == {url}')
    response = client.post(url, data={'name': NEW_LABEL_NAME})
    # client.post('/labels/1/update', data={'name': NEW_LABEL_NAME})
    assert response.url == '/login/' 


@pytest.mark.usefixtures('authorized_user')
@pytest.mark.django_db
def test_delete_label(client, label):
    url = DELETE_URL.format(id=label.id)
    logger.debug(f'label delete url == {url}')
    client.post(url)
    assert not Label.objects.filter(id=label.id).exists()


@pytest.mark.django_db
def test_delete_label_not_auth(client, label):
    url = DELETE_URL.format(id=label.id)
    logger.debug(f'label delete url == {url}')
    response = client.post(url)
    assert response.url == '/login/'
    assert Label.objects.filter(id=label.id).exists()