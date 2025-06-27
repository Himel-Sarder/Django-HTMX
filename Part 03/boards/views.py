from django.shortcuts import render
from django.http import HttpResponse
from .models import Board

def home(request):
    board = Board.objects.first()  # Just show the first board for now
    return render(request, 'boards/home.html', {'board': board})


def welcome_partial(request):
    return render(request, 'boards/partials/welcome_message.html')
