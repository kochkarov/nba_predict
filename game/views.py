from django.shortcuts import render
from django.views.generic import ListView
from .models import Game
from django.utils.timezone import now
from django.views.generic import MonthArchiveView, DayArchiveView, ArchiveIndexView


class TodayGameView(DayArchiveView):
    model = Game
    month_format = '%m'
    date_field = 'game_date'
    allow_future = True
    # context_object_name = 'championships'
    # queryset = Championship.objects.all().order_by('-name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Чемпионат прогнозов'
        return context
