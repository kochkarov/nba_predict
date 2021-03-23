from django.db import models

# Create your models here.


class Game(models.Model):
    game_id = models.IntegerField('Game ID')
    season = models.IntegerField('Season')
    game_date = models.DateTimeField('Game date')
    team_id_home = models.ForeignKey('team.Team', related_name='team_id_home', on_delete=models.CASCADE,
                                     verbose_name='Home team')
    team_id_visitor = models.ForeignKey('team.Team', related_name='team_id_visitor', on_delete=models.CASCADE,
                                        verbose_name='Visitor team')
    score_home = models.IntegerField('Home score')
    score_visitor = models.IntegerField('Visitor score')

    def __str__(self):
        return f'{self.team_id_home} {self.score_home}:{self.score_visitor} {self.team_id_visitor}'

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

