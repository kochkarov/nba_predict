from django.db import models

from team.models import Team


class Game(models.Model):
    """Класс Django с таблицей результатов игр"""
    is_win = models.IntegerField('Is win ?', null=True, default=None)
    game_id = models.CharField('Game ID', max_length=15, primary_key=True, db_index=True)
    season = models.IntegerField('Season', default=2020)
    game_date = models.DateField('Game date', default=None)
    game_time = models.TimeField('Game time', default=None)
    game_start_utc = models.DateTimeField('Game start UTC', default=None)
    team_home = models.ForeignKey('team.Team', related_name='+', on_delete=models.PROTECT,
                                  verbose_name='Home team', default=None)
    team_visitor = models.ForeignKey('team.Team', related_name='+', on_delete=models.PROTECT,
                                     verbose_name='Visitor team', default=None)
    team_name_home = models.CharField('Home name', max_length=3, default='')
    score_home = models.IntegerField('Home score')
    score_visitor = models.IntegerField('Visitor score')
    team_name_visitor = models.CharField('Visitor name', max_length=3, default='')
    boxscore = models.JSONField(null=True, verbose_name='Boxscore')
    stage_id = models.IntegerField('Stage ID', default=2)

    def __str__(self):
        return f'{self.game_date} {self.team_home} {self.score_home}:{self.score_visitor} {self.team_visitor}'

    def save(self, *args, **kwargs):
        self.is_win = self.get_is_win()
        super().save(*args, **kwargs)

    def get_is_win(self):
        if self.score_home > self.score_visitor:
            return 1
        elif self.score_home < self.score_visitor:
            return 0
        else:
            return None

    def human_repr(self):
        return f'{self.team_home.name}  {self.score_home}:{self.score_visitor} {self.team_visitor.name}'

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['-game_start_utc']
