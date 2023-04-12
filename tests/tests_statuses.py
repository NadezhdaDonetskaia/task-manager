from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages

from task_manager.statuses.models import Status


class StatusesTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')

    def test_create_status_authenticated(self):
        url = reverse('status_create')
        data = {'name': 'new_status', 'user': self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.data['name'], 'new_status')
        message = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]), 'Статус успешно создан')

    def test_create_status_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse('status_create'), {'name': 'new_status'})
        self.assertNotContains(response.data['name'], 'new_status')
        self.assertEqual(response.status_code, 302)
        message = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]), 'Надо войти в систему для создания статуса')

    def test_status_view_authenticated(self):
        url = reverse('statuses_list')
        response = self.client.get(url, {'user': self.user.pk})
        self.assertEqual(response.status_code, 200)

    def test_statuses_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('statuses_list'))
        self.assertEqual(response.status_code, 302)
        message = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]), 'Надо войти в систему для просмотра статусов')

    def test_status_update_authenticated(self):
        Status.objects.create(name='new_status', user=self.user)
        data = {'name': 'Updated status', 'user': self.user.pk}
        response = self.client.post(reverse('status_update', data))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.data['text'], 'Updated status')
        message = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]), 'Статус успешно обновлен')

    def test_status_update_unauthenticated(self):
        Status.objects.create(name='new_status', user=self.user)
        self.client.logout()
        response = self.client.post(reverse('status_update',  {'text': 'Updated status'}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.data['name'], 'new_status')
        message = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]), 'Надо войти в систему для изменения статуса')

    def test_status_delete_authenticated(self):
        Status.objects.create(name='new_status', user=self.user)
        response = self.client.post(reverse('status_delete'))
        self.assertEqual(response.status_code, 302)
        message = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]), 'Статус успешно удален')

    def test_status_delete_unauthenticated(self):
        Status.objects.create(name='new_status', user=self.user)
        self.client.logout()
        response = self.client.post(reverse('status_delete'))
        self.assertEqual(response.status_code, 302)
        message = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]), 'Надо войти в систему для удаления статуса')

