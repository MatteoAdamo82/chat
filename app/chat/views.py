from django.shortcuts import render, redirect
from .models import Room

def homepage(request):
    rooms = Room.objects.all()

    return render(request, 'chat/homepage.html', {'rooms': rooms})

