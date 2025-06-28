from django.http import HttpResponse
from .models import Board
from django.shortcuts import render, get_object_or_404
from .models import List, Task
from .forms import TaskForm

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
