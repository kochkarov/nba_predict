from django.db import models
from game.models import Game
from member.models import Member


# class Prediction(models.Model):
#     """Класс Django с таблицей прогнозов игр"""
#     game_date = models.DateField('Game date', default=None)
#     game = models.ForeignKey('game.Game', related_name='+', on_delete=models.CASCADE,
#                              verbose_name='Predicted game', default=None)
#     user = models.ForeignKey('member.Member', related_name='+', on_delete=models.CASCADE,
#                              verbose_name='Predicted game', default=None)
#     predict = models.IntegerField('Predict', default=None)
#
#     class Meta:
#         verbose_name = 'Прогноз'
#         verbose_name_plural = 'Прогнозы'
