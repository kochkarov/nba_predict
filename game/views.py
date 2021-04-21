from django.shortcuts import render
from django.views.generic import ListView
from .models import Game
from django.utils.timezone import now
from django.views.generic import MonthArchiveView, DayArchiveView, ArchiveIndexView


def index(request):
    return render(request, 'game/index.html')

