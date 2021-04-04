import requests
from team.models import Team, TeamSchema, Division, DivisionSchema, Conference
from game.models import Game, GameSchema, TeamScoreSchema
import pydantic
from jinja2 import Template

DOMAIN = 'http://data.nba.net'
START_PATH = '/10s/prod/v2/today.json'
SCHEDULE = '/prod/v1/{{season}}/schedule.json'


def add_season_key(list_of_dict: list, season: int) -> list:
    """ Добавляет в словарь ключ со значением сезона """
    for element in list_of_dict:
        element['season'] = season
        yield element


def set_code(cls):
    for i, obj in enumerate(cls.objects.order_by('name')):
        obj.code = i
        obj.save()
    return


def get_team_column_names(suffix='') -> list:
    return [f'{team.name}_{suffix}' for team in Team.objects.order_by('code')]


class ApiNba:

    def __init__(self):
        self.links = self.get_available_json_links()
        return

    @staticmethod
    def get_json(path):
        url = DOMAIN + path
        response = requests.request("GET", url)
        return response.json()

    def get_available_json_links(self):
        return self.get_json(START_PATH)['links']

    def create_teams(self):
        json = self.get_json(self.links['teams'])['league']['standard']
        _ = pydantic.parse_obj_as(list[DivisionSchema], json)
        _ = pydantic.parse_obj_as(list[TeamSchema], json)
        set_code(Conference)
        set_code(Division)
        set_code(Team)
        return

    def get_and_save_games(self, season: int):
        link = Template(SCHEDULE).render(season=season)
        game_list = self.get_json(link)['league']['standard']
        return pydantic.parse_obj_as(list[GameSchema], add_season_key(game_list, season))
