from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext
from django.shortcuts import redirect


def index(request):
    text = "Welcome to my site."
    name_app = 'Task manager'
    return render(request, 'index.html', context={
        'text': text,
        'name_app': name_app,
    })

# def index(request):
#     a = None
#     a.hello() # Creating an error with an invalid line of code
#     return HttpResponse("Hello, world. You're at the pollapp index.")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Старница не найдена</h1>')


class UserLoginRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, gettext('You are not authorized! Please sign in.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
