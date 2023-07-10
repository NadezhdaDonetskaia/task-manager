import pytest

from task_manager.tasks.models import Task, Label, Status, User
from task_manager.logger_config import logger

USER_PASSWORD = 'test_password'
USER_DATA = dict(
    username='test_user',
    first_name='Test',
    last_name='Testov'
)


@pytest.fixture
def user():
    user_model = User
    user_ = user_model.objects.create_user(USER_DATA)
    user_.set_password(USER_PASSWORD)
    user_.save()
    logger.debug(f'Create user {user_.username}')
    return user_


@pytest.fixture
def authorized_user(client, user):
    c = client.login(
        username=user.username,
        password=USER_PASSWORD
    )
    logger.debug(f'Login user {user.username}')
    logger.debug(f'clien login {c}')
    return user

@pytest.fixture
def status():
    status = Status.objects.create(name='Status test')
    return status


@pytest.fixture
def label():
    label = Label.objects.create(name='Label test')
    return label


@pytest.fixture
def task(user, status, label):
    task = Task.objects.create(
        name='Task test',
        author=user,
        executor=user,
        status=status,
        description='Description for test',
    )
    task.labels.add(label)
    return task