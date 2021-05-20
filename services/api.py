import requests
import pydantic
from jinja2 import Template
from tqdm.notebook import tqdm
from django.db.models import Avg

from game.models import Game
from championship.models import Prediction
from team.models import Team, TeamSchema, Division, DivisionSchema, Conference
from game.validate import GameSchema

DOMAIN = 'https://data.nba.net'
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
        self.current_season = self.get_current_season()
        return

    @staticmethod
    def get_json(path):
        url = DOMAIN + path
        response = requests.request("GET", url)
        return response.json()

    def get_current_season(self):
        key_str = self.links['teams']
        return int(key_str.split('/')[-2])

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

    def calc_rate_prediction(self, season=0):
        season = season if season else self.current_season
        games = Game.objects.filter(season=season)
        for game in tqdm(games):
            rate = Prediction.objects.filter(game=game).aggregate(rate=Avg('result'))['rate']
            Prediction.objects.filter(game=game, is_guessed=1).update(rate=rate)

    def check_prediction(self, season=0):
        season = season if season else self.current_season
        for predict in tqdm(Prediction.objects.filter(game__season=season, result__isnull=True,
                                                      game__is_win__isnull=False)):
            predict.result = 1 if predict.predict == predict.game.is_win else 0
            predict.save()
        return

    def update_data(self, season=0):
        season = season if season else self.current_season
        game_list = self.get_json(Template(SCHEDULE).render(season=season))['league']['standard']
        _ = pydantic.parse_obj_as(list[GameSchema], add_season_key(game_list, season))

        self.check_data(season=season)
        self.check_prediction(season=season)
        return

    def update_boxscore(self, season=0):
        season = season if season else self.current_season
        games = Game.objects.filter(season=season)
        for game in tqdm(games):
            game.boxscore = self.get_json(Template(self.links['boxscore']).render(
                gameId=game.game_id, gameDate=game.game_date.strftime('%Y%m%d')))
            game.save()
        return

    def check_data(self, season=0):
        season = season if season else self.current_season
        games = Game.objects.filter(season=season)
        for game in games:
            score_home = int(game.boxscore['basicGameData']['hTeam']['score'])
            if game.score_home != score_home:
                game.score_home = max(game.score_home, score_home)
                game.save()
                print(f'Corrected Home score error {game}')
            score_visitor = int(game.boxscore['basicGameData']['vTeam']['score'])
            if game.score_visitor != score_visitor:
                game.score_visitor = max(game.score_visitor, score_visitor)
                game.save()
                print(f'Corrected Visitor score error {game}')
