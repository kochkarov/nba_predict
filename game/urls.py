from django.urls import path, register_converter
from django.views.generic import DayArchiveView
from . import views, converters
from .models import Game

register_converter(converters.DateConverter, 'yyyy')

urlpatterns = [
    path('<int:year>/<int:month>/<int:day>/',
         DayArchiveView.as_view(model=Game, month_format='%m', date_field='game_date'),
         name='archive_day'),
]
