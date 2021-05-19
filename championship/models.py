import enum

from django.db import models

from game.models import Game
from member.models import Member


class Status(enum.IntEnum):
    UNKNOWN = 0
    SOON = 1
    IN_PROGRESS = 2
    ENDED = 3


class League(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('League name', max_length=42)

    def __str__(self):
        return self.name


class Championship(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.IntegerField('Championship status', default=Status.UNKNOWN)
    name = models.CharField('Championship name', max_length=142)
    league = models.ForeignKey('League', related_name='+', on_delete=models.CASCADE,
                               verbose_name='League', default=None)
    members = models.ManyToManyField('member.Member')
    games = models.ManyToManyField('game.Game')
    scoreboard = models.ForeignKey('Scoreboard', related_name='+', on_delete=models.CASCADE,
                                   verbose_name='Scoreboard', null=True, default=None)


class Scoreboard(models.Model):
    id = models.BigAutoField(primary_key=True)
    prediction = models.ForeignKey('prediction.Prediction', related_name='+', on_delete=models.CASCADE,
                                   verbose_name='Prediction', default=None)
    result = models.IntegerField('Guessed ?', null=True, default=None)
    rate = models.FloatField('Rating')
