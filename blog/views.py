from calendar import error

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required



def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'blog/task_list.html', {'tasks': tasks})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'blog/task_detail.html', {'task': task})



def task_new(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_date = timezone.now()
            task.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'blog/task_edit.html', {'form': form})



def task_edit(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")

    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_date = timezone.now()
            task.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'blog/task_edit.html', {'form': form})



def task_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")

    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        messages.success(request, "La tâche a été supprimée.")
        return redirect('task_list')
    return render(request, 'blog/task_delete.html', {'task': task})


def task_toggle_done(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = not task.status
    task.save()
    return redirect('task_detail', pk=pk)




from django.http import JsonResponse

def task_toggle_done_ajax(request, pk) :
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    if request.method == "POST" :
        task = get_object_or_404(Task, pk=pk)
        task.status = not task.status
        task.save()

        return JsonResponse({
            "status": task.status,
            "task_id": task.pk
        })




from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect

def c_login(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            error = "Nom d'utilisateur ou mot de passe incorrect"

    return render(request, "blog/login.html", {"error": error})


def c_logout(request):
    logout(request)
    return redirect("task_list")




