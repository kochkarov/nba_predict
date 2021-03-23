from django.db import models
from pydantic import BaseModel, Field, validator


class Conference(models.Model):
    conf_name = models.CharField('Conference name', max_length=4, default='West', unique=True)

    def __str__(self):
        return self.conf_name

    class Meta:
        verbose_name = 'Конференция'
        verbose_name_plural = 'Конференции'


class Division(models.Model):
    div_name = models.CharField('Division name', max_length=10, unique=True)
    div_conf = models.ForeignKey(Conference, on_delete=models.CASCADE, verbose_name='Conference')

    def __str__(self):
        return self.div_name

    class Meta:
        verbose_name = 'Дивизион'
        verbose_name_plural = 'Дивизионы'


class Team(models.Model):
    team_name_short = models.CharField('Short name', max_length=3, unique=True)
    team_name_full = models.CharField('Full name', max_length=80, unique=True)
    team_id = models.IntegerField('Team ID', unique=True)
    team_division = models.ForeignKey(Division, on_delete=models.CASCADE, verbose_name='Division')

    def __str__(self):
        return self.team_name_full

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'


class TeamSchema(BaseModel):
    team_name_short: str = Field(None, alias='tricode', max_length=3)
    team_name_full: str = Field(None, alias='fullName')
    team_id: int = Field(None, alias='teamId')
    team_division: Division = Field(None, alias='divName')

    class Config:
        arbitrary_types_allowed = True
        extra = 'ignore'

    @validator('team_division', pre=True)
    def convert_str_to_class(cls, value):
        return Division.objects.get(div_name=value)
