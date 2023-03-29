from django.shortcuts import render

from django.utils.translation import gettext


def index(request):
    text = gettext("Welcome to my site.")
    title = gettext('Title')
    name_app = gettext('Task manager')
    return render(request, 'index.html', context={
        'text': text,
        'title': title,
        'name_app': name_app,
    })
