from django.urls import reverse_lazy
import pytest
from task_manager.logger_config import logger
from tests.conftest import Task


CREATE_URL = reverse_lazy('task_create')
UPDATE_URL = 'task/{id}/update/'
DELETE_URL = 'task/{id}/delete/'
INPUT_DATA = dict(name='task_test')


@pytest.mark.usefixtures('authorized_user')
@pytest.mark.django_db
def test_create_task(client, label, status):
    response = client.post(CREATE_URL, data={'name': 'New Task',
                                             'label': label.id,
                                             'status': status.id})
    logger.debug(f'Resp task {response}')
    assert response.status_code == 302
    assert Task.objects.filter(name="New Task").exists()
