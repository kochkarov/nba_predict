from django.contrib import admin

from .models import Championship, League, Score, Event


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    readonly_fields = (['members'])


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    readonly_fields = (['games'])


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    readonly_fields = (['prediction'])


@admin.register(Championship)
class ChampionshipAdmin(admin.ModelAdmin):
    readonly_fields = (['scoreboard'])
