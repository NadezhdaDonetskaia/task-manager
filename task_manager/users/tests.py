from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages import get_messages
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase, Client
from django.contrib.auth.models import User
from django.utils.translation import gettext

from task_manager.users.views import UserRegistrationView, UserUpdateView, UserDeleteView


class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_registration_view_valid_form(self):
        request = self.factory.post(reverse_lazy('users_register'), data={
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe'
        })

        # Добавляем необходимые middleware для обработки сессий и сообщений
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Создаем экземпляр UserRegistrationView
        view = UserRegistrationView.as_view()

        # Отправляем запрос на view
        response = view(request)

        # Проверяем, что пользователь успешно зарегистрирован
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('home'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertEqual(str(response.context['message']), gettext('Вы успешно зарегистрировались!'))

    def test_registration_view_invalid_form(self):
        # Создаем POST-запрос с невалидными данными формы регистрации
        request = self.factory.post(reverse_lazy('users_register'), data={
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword2',  # Неверное подтверждение пароля
            'first_name': 'John',
            'last_name': 'Doe'
        })

        # Добавляем необходимые middleware для обработки сессий и сообщений
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Создаем экземпляр UserRegistrationView
        view = UserRegistrationView.as_view()

        # Отправляем запрос на view
        response = view(request)

        # Проверяем, что форма невалидна и в сообщениях есть ошибка
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertEqual(str(response.context['message']), gettext('Ошибка регистрации!'))


class UserUpdateViewTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('user_update', kwargs={'pk': self.user.pk})
        self.client = Client()
        self.client.defaults.update({'HTTP_REFERER': '/some/referer/'})

    def test_user_update_view_redirects_unauthenticated_user(self):
        # Test that unauthenticated user is redirected to login page
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + self.url)

    def test_user_update_view_displays_form(self):
        # Test that authenticated user can access the update form
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update Profile')

    def test_user_update_view_updates_user_profile(self):
        # Test that user profile is updated successfully
        self.client.login(username='testuser', password='testpassword')
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newuser')
        self.assertEqual(self.user.first_name, 'New')
        self.assertEqual(self.user.last_name, 'User')

    def test_user_update_view_with_different_user_raises_permission_denied(self):
        # Test that trying to update another user's profile raises PermissionDenied
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
        self.client.login(username='testuser', password='testpassword')
        url = reverse('user_update', args=[another_user.pk])
        with self.assertRaises(PermissionDenied):
            self.client.get(url)

    def test_user_update_view_with_unauthorized_user_redirects_to_referrer(self):
        # Test that unauthorized user is redirected to referrer URL
        self.client.login(username='testuser', password='testpassword')
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User'
        }
        url = reverse('user_update', args=[self.user.pk])
        self.client.logout()
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_user_update_view_with_valid_form_displays_success_message(self):
        # Test that success message is displayed when form is valid
        self.client.login(username='testuser', password='testpassword')
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        storage = get_messages(response.wsgi_request)
        self.assertIn('Информация обновлена!', [msg.message for msg in storage])

    def test_user_update_view_with_valid_form_updates_user_info(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'username': 'newuser',  # Valid data
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('user_update', kwargs={'pk': self.user.pk}))
        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.username, 'newuser')
        self.assertEqual(updated_user.first_name, 'New')
        self.assertEqual(updated_user.last_name, 'User')

    def test_user_update_view_with_invalid_form_displays_error_message(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'username': '',  # Invalid data
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        storage = get_messages(response.wsgi_request)
        self.assertIn('Ошибка обновления!', [msg.message for msg in storage])


class UserDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('user_delete', kwargs={'pk': self.user.pk})
        self.middleware = [
            MessageMiddleware,
            SessionMiddleware,
            AuthenticationMiddleware,
        ]

    def test_user_delete_view_get(self):
        # Test that GET request to UserDeleteView displays the delete confirmation page
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')
        self.assertContains(response, 'Вы действительно хотите удалить свой профиль?')

    def test_user_delete_view_post(self):
        # Test that POST request to UserDeleteView deletes the user and redirects to success URL
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.user.pk)

    def test_user_delete_view_post_with_different_user_raises_permission_denied(self):
        # Test that trying to delete another user's profile raises PermissionDenied
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
        self.client.login(username='testuser', password='testpassword')
        url = reverse('user_delete', args=[another_user.pk])
        with self.assertRaises(PermissionDenied):
            self.client.post(url)

    def test_user_delete_view_post_with_unauthenticated_user_redirects_to_login(self):
        # Test that trying to delete profile with unauthenticated user redirects to login page
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)

    def test_user_delete_view_post_with_invalid_form_displays_error_message(self):
        # Test that trying to delete profile with invalid form displays error message
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')
        self.assertContains(response, 'Ошибка удаления!')

    def test_user_delete_view_handle_no_permission_with_raise_exception_enabled_raises_permission_denied(self):
        # Test that handle_no_permission() raises PermissionDenied with raise_exception enabled
        request = self.client.post(self.url)
        request.user = self.user
        request.META['HTTP_REFERER'] = reverse('home')
        request.method = 'POST'
        request.session = self.client.session
        for middleware in self.middleware:
            middleware().process_request(request)
        view = UserDeleteView()
        view.raise_exception = True
        with self.assertRaises(PermissionDenied):
            view.handle_no_permission()

    def test_user_delete_view_get_success_url(self):
        # Test that get_success_url() returns the correct URL
        view = UserDeleteView()
        view.object = self.user
        success_url = view.get_success_url()
        self.assertEqual(success_url, reverse('user_delete', kwargs={'pk': self.user.pk}))

    def test_user_delete_view_test_func_with_authenticated_user_and_matching_pk_returns_true(self):
        # Test that test_func() returns True with authenticated user and matching pk
        request = self.client.get(self.url)
        request.user = self.user
        view = UserDeleteView()
        view.request = request
        view.kwargs = {'pk': self.user.pk}
        result = view.test_func()
        self.assertTrue(result)

    def test_user_delete_view_test_func_with_authenticated_user_and_non_matching_pk_returns_false(self):
        # Test that test_func() returns False with authenticated user and non-matching pk
        request = self.client.get(self.url)
        request.user = self.user
        view = UserDeleteView()
        view.request = request
        view.kwargs = {'pk': self.user.pk + 1}
        result = view.test_func()
        self.assertFalse(result)

    def test_user_delete_view_test_func_with_unauthenticated_user_returns_false(self):
        # Test that test_func() returns False with unauthenticated user
        request = self.client.get(self.url)
        request.user = AnonymousUser()
        view = UserDeleteView()
        view.request = request
        view.kwargs = {'pk': self.user.pk}
        result = view.test_func()
        self.assertFalse(result)

    def test_user_delete_view_form_invalid_displays_error_message(self):
        # Test that form_invalid() displays error message
        form = UserDeleteForm()
        view = UserDeleteView()
        view.request = self.client.post(self.url)
        view.form_invalid(form)
        messages = list(get_messages(view.request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Ошибка удаления!')

    def test_user_delete_view_delete_displays_success_message(self):
        # Test that delete() displays success message
        view = UserDeleteView()
        view.request = self.client.post(self.url)
        view.delete(view.request)
        messages = list(get_messages(view.request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Пользователь удален!')