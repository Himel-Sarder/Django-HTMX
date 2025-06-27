from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'boards/home.html')

def welcome_partial(request):
    return render(request, 'boards/partials/welcome_message.html')
