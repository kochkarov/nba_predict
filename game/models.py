import datetime
from zoneinfo import ZoneInfo
from typing import Union

from django.db import models
from pydantic import BaseModel, Field, root_validator

from team.models import Team


class TeamScoreSchema(BaseModel):
    team_id: int = Field(None, alias='teamId')
    score: Union[int, str] = Field(None, alias='score')


class GameSchema(BaseModel):
    """Класс Pydantic для парсинга результатов игр"""
    game_id: int = Field(None, alias='gameId')
    stage_id: int = Field(None, alias='seasonStageId')
    season: int = Field(None)
    game_start_utc: datetime.datetime = Field(None, alias='startTimeUTC')
    team_home: TeamScoreSchema = Field(None, alias='hTeam')
    team_visitor: TeamScoreSchema = Field(None, alias='vTeam')

    class Config:
        arbitrary_types_allowed = True
        extra = 'ignore'

    @root_validator(skip_on_failure=True)
    def check_and_save_game(cls, values):
        if values.get('stage_id') != 2:
            return values

        us_time = values['game_start_utc'].astimezone(ZoneInfo('US/Central'))
        game_dict = {**values, 'game_date': us_time.date(), 'game_time': us_time.time(),
                     'team_home': Team.objects.get(team_id=values['team_home'].team_id),
                     'team_visitor': Team.objects.get(team_id=values['team_visitor'].team_id),
                     'score_home': values['team_home'].score, 'score_visitor': values['team_visitor'].score}

        game_dict['team_name_home'] = game_dict['team_home'].name
        game_dict['team_name_visitor'] = game_dict['team_visitor'].name

        new_game, _ = Game.objects.get_or_create(**game_dict)
        print(new_game)
        return values


class Game(models.Model):
    """Класс Django с таблицей результатов игр"""
    game_id = models.IntegerField('Game ID')
    stage_id = models.IntegerField('Stage ID', default=2)
    season = models.IntegerField('Season', default=2020)
    game_date = models.DateField('Game date', default=None)
    game_time = models.TimeField('Game time', default=None)
    game_start_utc = models.DateTimeField('Game start UTC', default=None)
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

    def human_repr(self):
        return f'{self.team_home.name}  {self.score_home}:{self.score_visitor} {self.team_visitor.name}'

    def is_win(self):
        return 1 if self.score_home > self.score_visitor else 0

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
