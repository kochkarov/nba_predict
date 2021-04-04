import pandas as pd
import numpy as np
from game.models import Game
from team.models import Team


class DataNba:

    def __init__(self):
        self.data = pd.DataFrame()
        self._temp = pd.DataFrame()
        self.games = Game.objects.filter(season=2020)
        # self.games = Game.objects.all()
        self.teams = Team.objects.all()

        self.create_base_column()
        self.add_mirror()
        return

    def create_base_column(self):
        columns = ['game_id', 'season', 'date', 'human', 'team', 'opponent', 'score_team', 'score_opp']
        self.data = pd.DataFrame([[game.game_id, game.season, game.game_date, game.human_repr(),
                                   game.team_home.code, game.team_visitor.code,
                                   game.score_home, game.score_visitor] for game in self.games],
                                 columns=columns)

        self.data['is_home_game'] = 1
        self.data['is_guest_game'] = 0

        self.data['is_win'] = np.where(self.data.score_team > self.data.score_opp, 1, 0)
        self.data['is_lose'] = 1 - self.data.is_win
        return

    def swap_column(self):
        swap_dict = {'team': 'opponent', 'score_team': 'score_opp', 'is_home_game': 'is_guest_game',
                     'is_win': 'is_lose'}

        columns = self.data.columns.copy(deep=True)
        for key, value in swap_dict.items():
            ind1, ind2 = columns.get_loc(key), columns.get_loc(value)
            columns.values[ind2], columns.values[ind1] = columns.values[ind1], columns.values[ind2]
        return columns

    def add_mirror(self):
        mirror = self.data.copy()
        mirror.columns = self.swap_column()
        mirror = mirror[self.data.columns]
        self.data = self.data.append(mirror,  ignore_index=True).sort_values(by=['date', 'game_id', 'is_guest_game'])
        return

    def add_features(self):
        pass
        # self.data['is_home_win'] = self.data.is_win
        # self.data['is_home_lose'] = self.data.is_lose
        # self.data['is_guest_win'] =
