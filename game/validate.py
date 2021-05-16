import datetime
from zoneinfo import ZoneInfo
from typing import Union

from .models import Game
from team.models import Team

from pydantic import BaseModel, Field, root_validator


class TeamScoreSchema(BaseModel):
    team_id: int = Field(None, alias='teamId')
    score: Union[int, str] = Field(None, alias='score')

    @root_validator(skip_on_failure=True)
    def check_score(cls, values):
        values['score'] = values['score'] if isinstance(values['score'], int) else 0
        return values


class GameSchema(BaseModel):
    """Класс Pydantic для парсинга результатов игр"""
    game_id: str = Field(None, alias='gameId')
    stage_id: int = Field(None, alias='seasonStageId')
    season: int = Field(None)
    game_start_utc: Union[datetime.datetime, str] = Field(None, alias='startTimeUTC')
    team_home: TeamScoreSchema = Field(None, alias='hTeam')
    team_visitor: TeamScoreSchema = Field(None, alias='vTeam')

    class Config:
        arbitrary_types_allowed = True
        extra = 'ignore'

    @root_validator(skip_on_failure=True)
    def check_and_save_game(cls, values):
        if values.get('stage_id') != 2:
            return values

        if not isinstance(values['game_start_utc'], datetime.datetime):
            values['game_start_utc'] = datetime.datetime.strptime(values['game_start_utc'], '%Y-%m-%d')

        us_time = values['game_start_utc'].astimezone(ZoneInfo('US/Central'))
        game_dict = {**values, 'game_date': us_time.date(), 'game_time': us_time.time(),
                     'team_home': Team.objects.get(team_id=values['team_home'].team_id),
                     'team_visitor': Team.objects.get(team_id=values['team_visitor'].team_id),
                     'score_home': values['team_home'].score, 'score_visitor': values['team_visitor'].score}

        game_dict['team_name_home'] = game_dict['team_home'].name
        game_dict['team_name_visitor'] = game_dict['team_visitor'].name

        obj, created = Game.objects.update_or_create(game_id=game_dict['game_id'], defaults=game_dict)
        if created:
            print(f'{obj}')
        return values
