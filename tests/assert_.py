from urllib.parse import urlparse
from django.urls import reverse

REDIRECT_STATUS_CODE = 302


def redirect_to(response, url):
    assert (
        response.status_code == REDIRECT_STATUS_CODE
   ), f'Expected status_code {REDIRECT_STATUS_CODE},' \
      f'but received {response.status_code}'
    redirect_url = urlparse(response.url).path
    return redirect_url == url


def redirect_to_login(response):
    return redirect_to(response, reverse('login'))
