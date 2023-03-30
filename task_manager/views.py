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
