from copy import copy
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import pytest

from task_manager.logger_config import logger

USER_PASSWORD = 'test_password'
USER_DATA = dict(
    username='test_user',
    first_name='Test',
    last_name='Testov'
)



@pytest.fixture
def input_data(request):
    return copy(request.module.INPUT_DATA)


@pytest.fixture
def create_object(model, input_data):

    def create(**kwargs):
        input_data.update(kwargs)
        obj = model(**input_data)
        obj.save()
        logger.error(f'Create obj {obj}')
        return obj
    return create


@pytest.fixture
def created_object(create_object):
    return create_object()


@pytest.fixture
def user():
    user_model = get_user_model()
    user_ = user_model.objects.create_user(USER_DATA)
    user_.set_password(USER_PASSWORD)
    user_.save()
    logger.error(f'Create user {user_.username}')
    return user_


@pytest.fixture
def logged_in_user(client, user):
    c = client.login(
        username=user.username,
        password=USER_PASSWORD
    )
    logger.error(f'Login user {user.username}')
    logger.error(c)
    return user


@pytest.fixture
def authorized(logged_in_user):
    pass
