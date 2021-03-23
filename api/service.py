import requests
from team.models import Team, TeamSchema
import pydantic

DOMAIN = 'http://data.nba.net'
START_PATH = '/10s/prod/v2/today.json'


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

    def add_teams(self):
        json = self.get_json(self.links['teams'])['league']['standard']
        all_teams = pydantic.parse_obj_as(list[TeamSchema], json)
        for team_schema in all_teams:
            Team.objects.get_or_create(**team_schema.dict())
        return
