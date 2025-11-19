from django.shortcuts import render
from .models import Task


def post_list(request):
    tasks = Task.objects.all()
    return render(request, 'blog/post_list.html', {'tasks': tasks})
