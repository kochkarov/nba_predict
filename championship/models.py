import enum

from django.db import models
from django.db.models import Max, Min, F

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
        agg = self.games.all().aggregate(date_min=Min('game_date'), date_max=Max('game_date'))
        return f'Games from {agg["date_min"]} to {agg["date_max"]} ({len(self.games.all())} games)'


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

    def get_next(self):
        return Championship.objects.all().filter(pk__gt=self.pk).order_by('pk').first()

    def get_previous(self):
        return Championship.objects.all().filter(pk__lt=self.pk).order_by('-pk').first()

    def start(self):
        agg = self.event.games.all().aggregate(start=Min('game_date'))
        return f'{agg["start"]}'


        return

    def get_predict_list(self):
        """
        Возвращает список из трех элементов: игра, прогнозы на победу, прогнозы на поражение
        :return:
        """
        games = self.event.games.all().order_by('game_start_utc')
        qs = self.scoreboard.values(game=F('prediction__game_id'), member=F('prediction__member__name'),
                                    predict=F('prediction__predict'))

        win_list = [', '.join(qs.filter(predict=1, game=game.game_id).values_list('member', flat=True))
                    for game in games]
        lose_list = [', '.join(qs.filter(predict=0, game=game.game_id).values_list('member', flat=True))
                     for game in games]
        return zip(games, win_list, lose_list)


class Score(models.Model):
    id = models.BigAutoField(primary_key=True)
    prediction = models.ForeignKey('Prediction', related_name='+', on_delete=models.PROTECT,
                                   verbose_name='Prediction', default=None)
    result = models.IntegerField('Guessed ?', null=True, default=None)
    rate = models.FloatField('Rating', null=True, default=0)

    def __str__(self):
        return f'\n{self.prediction}  result:{self.result}  rating:{self.rate}'


class Prediction(models.Model):
    """Класс Django с таблицей прогнозов игр"""
    id = models.BigAutoField(primary_key=True)
    game = models.ForeignKey('game.Game', on_delete=models.PROTECT,
                             verbose_name='Predicted game', default=None, db_index=True)
    member = models.ForeignKey('member.Member', related_name='+', on_delete=models.PROTECT,
                               verbose_name='Member', default=None, db_index=True)
    predict = models.IntegerField('Predict', default=None)

    def __str__(self):
        return f'User: {self.member}, predict {self.predict}    {self.game}'

    class Meta:
        verbose_name = 'Прогноз'
        verbose_name_plural = 'Прогнозы'
        ordering = ['-game__game_date']
