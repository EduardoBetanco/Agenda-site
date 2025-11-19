from django.shortcuts import render, get_object_or_404
from .models import Task


def post_list(request):
    tasks = Task.objects.all()
    return render(request, 'blog/post_list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'blog/task_detail.html', {'task': task})
