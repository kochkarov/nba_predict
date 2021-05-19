from django.db import models
from game.models import Game
from member.models import Human, Member


class Prediction(models.Model):
    """Класс Django с таблицей прогнозов игр"""
    id = models.BigAutoField(primary_key=True)
    game = models.ForeignKey('game.Game', on_delete=models.CASCADE,
                             verbose_name='Predicted game', default=None, db_index=True)
    member = models.ForeignKey('member.Member', related_name='+', on_delete=models.CASCADE,
                               verbose_name='Member', default=None, db_index=True)
    predict = models.IntegerField('Predict', default=None)

    def __str__(self):
        good = '+' if self.result else ''
        return f'{good} User: {self.member}, predict {self.predict}    {self.game}'

    class Meta:
        verbose_name = 'Прогноз'
        verbose_name_plural = 'Прогнозы'
        ordering = ['-game_date']
