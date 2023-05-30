from copy import copy
from django.contrib.auth import get_user_model
import pytest


USER_DATA = dict(
    username='test_user',
    first_name='Test',
    last_name='Testov',
)
USER_PASSWORD = 'test_password'


@pytest.fixture
def input_data(request):
    return copy(request.module.INPUT_DATA)


@pytest.fixture
def create_object(model, input_data):

    def create(**kwargs):
        input_data.update(kwargs)
        obj = model(**input_data)
        obj.save()
        return obj
    return create


@pytest.fixture
def created_object(create_object):
    return create_object()


@pytest.fixture
def user():
    user_model = get_user_model()
    user_ = user_model.objects.create_user(USER_DATA)
    user_.save()
    return user_


@pytest.fixture
def logged_in_user(client, user):
    client.login(
        username=user.username,
        password=USER_PASSWORD
    )
    return user


@pytest.fixture
def authorized(logged_in_user):
    pass
