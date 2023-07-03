from django.http import HttpResponseNotFound
from django.shortcuts import render


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
