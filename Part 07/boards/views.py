from django.http import HttpResponse
from .models import Board
from django.shortcuts import render, get_object_or_404
from .models import List, Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.utils import timezone

def home(request):
    board = Board.objects.first()  # Just show the first board for now
    return render(request, 'boards/home.html', {'board': board})


def welcome_partial(request):
    return render(request, 'boards/partials/welcome_message.html')



def add_task(request, list_id):
    list_obj = get_object_or_404(List, id=list_id)

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.list = list_obj
            task.save()
            return render(request, 'boards/partials/task_card.html', {'task': task})

    form = TaskForm()
    return render(request, 'boards/partials/task_form.html', {'form': form, 'list_id': list_id})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    list_obj = task.list  # keep reference before deleting
    task.delete()

    # Return updated list of tasks as a fragment
    tasks = list_obj.tasks.all()
    return render(request, 'boards/partials/task_list.html', {
        'tasks': tasks,
        'list_id': list_obj.id
    })


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return render(request, 'boards/partials/task_card.html', {'task': task})

    form = TaskForm(instance=task)
    return render(request, 'boards/partials/task_edit_form.html', {
        'form': form,
        'task_id': task_id,
        'task': task  # Pass task to template
    })

@require_http_methods(["POST"])
def toggle_task_completion(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = not task.is_completed
    task.completed_at = timezone.now() if task.is_completed else None
    task.save()
    return render(request, 'boards/partials/task_card.html', {'task': task})