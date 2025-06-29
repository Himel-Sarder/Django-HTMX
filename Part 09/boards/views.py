from django.http import HttpResponse
from .models import Board
from django.shortcuts import render, get_object_or_404
from .models import List, Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json


def home(request):
    board = Board.objects.first()
    filter_type = request.GET.get('filter', 'all')  # Get filter from URL or default to 'all'

    context = {
        'board': board,
        'filter_type': filter_type  # Make sure this is passed
    }

    if request.headers.get('HX-Request'):
        lists = []
        for list_obj in board.lists.all():
            tasks = list_obj.tasks.all()

            if filter_type == 'active':
                tasks = tasks.filter(is_completed=False)
            elif filter_type == 'completed':
                tasks = tasks.filter(is_completed=True)

            list_obj.filtered_tasks = tasks
            lists.append(list_obj)

        return render(request, 'boards/partials/filtered_lists.html', {
            'board': board,
            'lists': lists,
            'filter_type': filter_type
        })

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

from django.http import JsonResponse

def filter_tasks(request, list_id, status):
    task_list = get_object_or_404(TaskList, id=list_id)

    if status == "completed":
        tasks = task_list.tasks.filter(is_completed=True)
    elif status == "active":
        tasks = task_list.tasks.filter(is_completed=False)
    else:
        tasks = task_list.tasks.all()

    return render(request, "boards/partials/task_list.html", {
        "task_list": task_list,
        "tasks": tasks
    })


@csrf_exempt
def reorder_tasks(request, list_id):
    if request.method == "POST":
        data = json.loads(request.body)
        task_ids = data.get('task_ids', [])

        for index, task_id in enumerate(task_ids):
            Task.objects.filter(id=task_id, list_id=list_id).update(order=index)

        return JsonResponse({'status': 'success'})
