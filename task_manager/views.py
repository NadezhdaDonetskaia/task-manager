from django.http import HttpResponseNotFound
from django.shortcuts import render


def index(request):
    text = "Welcome to my site."
    title = 'Title'
    name_app = 'Task manager'
    return render(request, 'index.html', context={
        'text': text,
        'title': title,
        'name_app': name_app,
    })


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Старница не найдена</h1>')

