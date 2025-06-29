from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST, require_http_methods
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Board, List, Task
from .forms import TaskForm, ListForm
import json

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Board


def home(request):
    # Get the first board or return 404 if no boards exist
    board = Board.objects.prefetch_related('lists__tasks').first()
    if not board:
        return render(request, 'boards/no_boards.html')  # Create this template if needed

    filter_type = request.GET.get('filter', 'all')

    if request.headers.get('HX-Request'):
        lists = []
        for list_obj in board.lists.all():
            tasks = list_obj.tasks.all()

            if filter_type == 'active':
                tasks = tasks.filter(is_completed=False)
            elif filter_type == 'completed':
                tasks = tasks.filter(is_completed=True)
            elif filter_type == 'overdue':
                tasks = tasks.filter(
                    is_completed=False,
                    due_date__lt=timezone.now().date()
                )

            list_obj.filtered_tasks = tasks.order_by('order')
            lists.append(list_obj)

        return render(request, 'boards/partials/filtered_list.html', {
            'lists': lists,
            'filter_type': filter_type
        })

    return render(request, 'boards/home.html', {
        'board': board,
        'filter_type': filter_type
    })

@require_http_methods(["POST"])
def add_list(request):
    board = Board.objects.first()
    form = ListForm(request.POST)

    if form.is_valid():
        list_obj = form.save(commit=False)
        list_obj.board = board
        list_obj.order = board.lists.count()
        list_obj.save()
        return redirect('home')

    return render(request, 'boards/home.html', {
        'board': board,
        'list_form': form
    })


@require_http_methods(["POST"])
def add_task(request, list_id):
    list_obj = get_object_or_404(List, id=list_id)
    form = TaskForm(request.POST)

    if form.is_valid():
        task = form.save(commit=False)
        task.list = list_obj
        task.order = list_obj.tasks.count()
        task.save()
        return render(request, 'boards/partials/task_card.html', {'task': task})

    return render(request, 'boards/partials/task_form.html', {
        'form': form,
        'list_id': list_id
    })


@require_http_methods(["DELETE"])
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    list_obj = task.list
    task.delete()

    tasks = list_obj.tasks.order_by('order')
    return render(request, 'boards/partials/task_list.html', {
        'tasks': tasks,
        'list_id': list_obj.id
    })


@require_http_methods(["GET", "POST"])
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return render(request, 'boards/partials/task_card.html', {'task': task})
    else:
        form = TaskForm(instance=task)

    return render(request, 'boards/partials/task_edit.html', {
        'form': form,
        'task': task
    })


@require_POST
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = not task.is_completed
    task.completed_at = timezone.now() if task.is_completed else None
    task.save()
    return render(request, 'boards/partials/task_card.html', {'task': task})


@csrf_exempt
@require_POST
def reorder_tasks(request, list_id):
    try:
        data = json.loads(request.body)
        task_ids = data.get('task_ids', [])

        with transaction.atomic():
            for index, task_id in enumerate(task_ids):
                Task.objects.filter(id=task_id, list_id=list_id).update(order=index)

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
@require_POST
def reorder_lists(request):
    try:
        data = json.loads(request.body)
        list_ids = data.get('list_ids', [])

        with transaction.atomic():
            for index, list_id in enumerate(list_ids):
                List.objects.filter(id=list_id).update(order=index)

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)