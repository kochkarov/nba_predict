from django.db import models
from django.utils.timezone import now

from team.models import Team


class Game(models.Model):
    """Класс Django с таблицей результатов игр"""
    game_id = models.CharField('Game ID', max_length=15, primary_key=True)
    stage_id = models.IntegerField('Stage ID', default=2)
    season = models.IntegerField('Season', default=2020)
    game_date = models.DateField('Game date', default=None)
    game_time = models.TimeField('Game time', default=None)
    game_start_utc = models.DateTimeField('Game start UTC', default=None)
    added = models.DateTimeField(default=now, blank=True)
    team_home = models.ForeignKey('team.Team', related_name='+', on_delete=models.CASCADE,
                                  verbose_name='Home team', default=None)
    team_visitor = models.ForeignKey('team.Team', related_name='+', on_delete=models.CASCADE,
                                     verbose_name='Visitor team', default=None)
    team_name_home = models.CharField('Home name', max_length=3, default='')
    score_home = models.IntegerField('Home score')
    score_visitor = models.IntegerField('Visitor score')
    team_name_visitor = models.CharField('Visitor name', max_length=3, default='')

    def __str__(self):
        return f'{self.game_date} {self.team_home} {self.score_home}:{self.score_visitor} {self.team_visitor}'

    def is_win(self):
        return self.score_home > self.score_visitor

    def human_repr(self):
        return f'{self.team_home.name}  {self.score_home}:{self.score_visitor} {self.team_visitor.name}'

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['game_id']
