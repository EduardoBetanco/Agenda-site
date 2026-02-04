from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Task
from .forms import TaskForm
from django.contrib import messages



def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'blog/task_list.html', {'tasks': tasks})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'blog/task_detail.html', {'task': task})


def task_new(request):
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
    if request.method == "POST" :
        task = get_object_or_404(Task, pk=pk)
        task.status = not task.status
        task.save()

        return JsonResponse({
            "status": task.status,
            "task_id": task.pk
        })



import ollama
from django.shortcuts import render

def ollama_test(request):
    description = ""

    tasks = Task.objects.all()
    if not tasks:
        description = "Il n'y a aucune tâche dans l'agenda."
    else:

        task_texts = []
        for t in tasks:
            status = "fait" if t.status else "non fait"
            task_texts.append(
                f"- {t.title} (Sujet: {t.subject}, Date: {t.due_date}, Statut: {status})\n  Description: {t.description}")
        tasks_summary = "\n".join(task_texts)


        prompt = (f"Voici la liste des tâches dans l'agenda :\n{tasks_summary}\n"
                  f"Pourrais tu me proposer un ordre dans lequel je devrait effectuer ces tâches et m'expliqer pourquoi tu a choisis cette ordre, réponse en français.")

        try:
            response = ollama.chat(model="llama2", messages=[{"role": "user", "content": prompt}])
            if hasattr(response, 'message') and hasattr(response.message, 'content'):
                description = response.message.content
            else:
                description = str(response)
        except Exception as e:
            description = f"Erreur lors de l'appel à l'API Ollama : {str(e)}"

    return render(request, 'blog/ollama_test.html', {'response_text': description})