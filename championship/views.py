from django.db.models import Avg, F, Sum, Count
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from .models import Championship


class ChampionshipListView(ListView):
    model = Championship
    context_object_name = 'championships'
    queryset = Championship.objects.all().order_by('-name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Чемпионат прогнозов'
        return context


class ChampionshipDetailView(DetailView):
    model = Championship
    context_object_name = 'championship'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['predicts'] = self.object.get_predict_list()
        context['table'] = self.object.scoreboard.all().values(name=F('prediction__member__name')).annotate(
            percent=Avg('result')*100, rating=Avg('rate'), res=Sum('result'), total=Count('result')
        ).order_by('-res')
        return context
