from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages


class UserTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_user(self):
        self.assertIsNotNone(self.user)
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpassword'))

    def test_authentication(self):
        response = self.client.post('/users/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_user_update_by_owner(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('user_update', args=[self.user.pk])
        data = {
            'username': 'updatedusername',
            'first_name': 'Updated',
            'last_name': 'User',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updatedusername')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')

    def test_user_update_by_non_owner(self):
        User.objects.create_user(username='anotheruser', password='anotherpassword')
        self.client.login(username='anotheruser', password='anotherpassword')
        url = reverse('user_update', args=[self.user.pk])
        response = self.client.post(url, HTTP_REFERER=url)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user)
        message = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]), 'У вас нет прав для изменения этого профиля.')

    def test_user_delete_by_owner(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('user_delete', args=[self.user.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(User.DoesNotExist):
            self.user.refresh_from_db()

    def test_user_delete_by_non_owner(self):
        User.objects.create_user(username='anotheruser', password='anotherpassword')
        self.client.login(username='anotheruser', password='anotherpassword')
        url = reverse('user_delete', args=[self.user.pk])
        response = self.client.post(url, HTTP_REFERER=url)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user)
        message = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(str(message[0]), 'У вас нет прав для удаления этого профиля.')
