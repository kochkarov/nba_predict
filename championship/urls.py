from django.urls import path, register_converter
from .models import Game
from .views import ChampionshipListView, ChampionshipDetailView

urlpatterns = [
    path('', ChampionshipListView.as_view(), name='championship'),
    path('<int:pk>/', ChampionshipDetailView.as_view(), name='championship-detail')
]
