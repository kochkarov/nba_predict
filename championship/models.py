import enum

from django.db import models

from game.models import Game
from member.models import Member


class Status(enum.IntEnum):
    UNKNOWN = 0
    SOON = 1
    IN_PROGRESS = 2
    ENDED = 3


class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('Event name', max_length=42)
    games = models.ManyToManyField('game.Game', related_name='games')

    def __str__(self):
        return f'{self.name} ({len(self.games.all())} games)'


class League(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('League name', max_length=42)
    members = models.ManyToManyField('member.Member', related_name='members')

    def __str__(self):
        return f'{self.name} ({len(self.members.all())} members)'


class Championship(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('Championship name', max_length=142)
    event = models.ForeignKey('Event', related_name='+', on_delete=models.PROTECT,
                              verbose_name='Event', null=True, default=None)
    status = models.IntegerField('Championship status', default=Status.UNKNOWN)
    league = models.ForeignKey('League', related_name='+', on_delete=models.PROTECT,
                               verbose_name='League', default=None)
    scoreboard = models.ManyToManyField('Score', related_name='scoreboard')

    def __str__(self):
        return self.name


class Score(models.Model):
    id = models.BigAutoField(primary_key=True)
    prediction = models.ForeignKey('prediction.Prediction', related_name='+', on_delete=models.PROTECT,
                                   verbose_name='Prediction', default=None)
    result = models.IntegerField('Guessed ?', null=True, default=None)
    rate = models.FloatField('Rating', null=True, default=0)

    def __str__(self):
        return f'{self.prediction}  result:{self.result}  rating:{self.rate}'
