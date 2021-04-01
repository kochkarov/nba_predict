from django.db import models
from pydantic import BaseModel, Field, validator
import numpy as np


class BaseTeamModel(models.Model):
    number = 30
    code = models.IntegerField('Code', default=-1)
    name = models.CharField('Name', max_length=42, unique=True, default='')

    def one_hot(self) -> list:
        return np.eye(self.number)[self.code].astype(int)


class Conference(BaseTeamModel):
    number = 2

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Конференция'
        verbose_name_plural = 'Конференции'


class Division(BaseTeamModel):
    number = 6
    div_conf = models.ForeignKey(Conference, on_delete=models.CASCADE, verbose_name='Conference')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дивизион'
        verbose_name_plural = 'Дивизионы'


class DivisionSchema(BaseModel):
    conference: str = Field(None, alias='confName')
    division: str = Field(None, alias='divName')

    class Config:
        extra = 'ignore'

    @validator('division', pre=True)
    def create_conf_and_div(cls, value, values):
        conf, _ = Conference.objects.get_or_create(name=values['conference'])
        Division.objects.get_or_create(name=value, div_conf=conf)
        return value


class Team(BaseTeamModel):
    number = 30
    name_full = models.CharField('Full name', max_length=80, unique=True)
    team_id = models.IntegerField('Team ID', unique=True)
    team_division = models.ForeignKey(Division, on_delete=models.CASCADE, verbose_name='Division')
    team_conference = models.ForeignKey(Conference, on_delete=models.CASCADE, verbose_name='Conference')

    def __str__(self):
        return self.name_full

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'


class TeamSchema(BaseModel):
    name: str = Field(None, alias='tricode', max_length=3)
    name_full: str = Field(None, alias='fullName')
    team_id: int = Field(None, alias='teamId')
    team_conference: Conference = Field(None, alias='confName')
    team_division: Division = Field(None, alias='divName')

    class Config:
        arbitrary_types_allowed = True
        extra = 'ignore'

    @validator('team_conference', pre=True)
    def convert_str_to_conf(cls, value):
        return Conference.objects.get(name=value)

    @validator('team_division', pre=True)
    def create_team(cls, value, values):
        div = Division.objects.get(name=value)
        values['team_division'] = div
        Team.objects.get_or_create(**values)
        return div
