import pandas as pd
import numpy as np
import re
from game.models import Game
from team.models import Team


class DataNba:
    teams = None
    game_objects = None
    team_objects = None
    data = None

    def __init__(self):
        if DataNba.data is None:
            self.init_data()
        return

    @classmethod
    def init_data(cls):
        cls.create_teams()
        cls.create_games()
        cls.add_mirrored_data()
        cls.add_total_columns()
        cls.add_onehot_columns(['team', 'opponent'])
        cls.add_last_result_columns('team', 'is_win', 20)
        cls.add_last_result_columns('opponent', 'is_win', 20)

    @classmethod
    def create_teams(cls):
        cls.team_objects = Team.objects.all()
        cls.teams = pd.DataFrame([[team.code, team.name, team.team_conference.code]
                                  for team in cls.team_objects], columns=['code', 'name', 'conference'])
        cls.teams.set_index('code', inplace=True)
        return

    @classmethod
    def create_games(cls):
        print('Create DataFrame...')
        cls.game_objects = Game.objects.all()

        columns = ['game_id', 'season', 'date', 'added', 'human', 'team', 'opponent', 'score_team', 'score_opp']
        cls.data = pd.DataFrame([[game.game_id, game.season, pd.Timestamp(game.game_date), pd.Timestamp(game.added),
                                  game.human_repr(), game.team_home.code, game.team_visitor.code,
                                  game.score_home, game.score_visitor] for game in cls.game_objects],
                                columns=columns)

        cls.data['is_home_game'] = 1
        cls.data['is_road_game'] = 0
        cls.data['is_win'] = np.where(cls.data.score_team > cls.data.score_opp, 1, 0)
        cls.data['is_lose'] = 1 - cls.data.is_win
        cls.data['is_home_win'] = cls.data.is_win
        cls.data['is_home_lose'] = 1 - cls.data.is_home_win
        cls.data['is_road_win'] = 0
        cls.data['is_road_lose'] = 0
        return

    @classmethod
    def add_onehot_columns(cls, columns: list):
        cls.data = cls.data.join(pd.get_dummies(cls.data[columns].astype('category'), prefix_sep='_oh_'))
        return

    @classmethod
    def swap_column(cls):
        swap_dict = {'team': 'opponent', 'score_team': 'score_opp', 'is_home_game': 'is_road_game',
                     'is_win': 'is_lose', 'is_home_win': 'is_road_lose', 'is_home_lose': 'is_road_win'}

        columns = cls.data.columns.copy(deep=True)
        for key, value in swap_dict.items():
            ind1, ind2 = columns.get_loc(key), columns.get_loc(value)
            columns.values[ind2], columns.values[ind1] = columns.values[ind1], columns.values[ind2]
        return columns

    @classmethod
    def add_mirrored_data(cls):
        mirror = cls.data.copy()
        mirror.columns = cls.swap_column()
        mirror = mirror[cls.data.columns]
        cls.data = cls.data.append(mirror, ignore_index=True).sort_values(by=['date', 'game_id', 'is_road_game'],
                                                                          ignore_index=True)
        return

    @classmethod
    def get_columns(cls, mask: str):
        return list(filter(re.compile(mask).search, cls.data.columns))

    @classmethod
    def add_total_columns(cls):
        columns = cls.get_columns('is_')
        for season in cls.data.season.unique():
            for team in cls.teams.index:
                idx = (cls.data.season == season) & (cls.data.team == team)
                for column in columns:
                    cls.data.loc[idx, column.replace('is_', 'total_')] = \
                        cls.data.loc[idx, column].cumsum().shift(fill_value=0)
        return

    @classmethod
    def get_last_result(cls, row, filter_column, data_column, count):
        return cls.data[data_column][(cls.data['date'] < row['date']) &
                                     (cls.data[filter_column] == row[filter_column]) &
                                     (cls.data.season == row.season)].values[:-count-1:-1]

    @classmethod
    def add_last_result_columns(cls, filter_column, data_column, count=20):
        hg = cls.data[cls.data.is_home_game == 1]
        result = pd.DataFrame([cls.get_last_result(row, filter_column, data_column, count) for _, row in hg.iterrows()],
                              index=hg.index, columns=cls.generate_names(filter_column, data_column, count))
        cls.data = cls.data.join(result)
        return

    @staticmethod
    def generate_names(filter_column, data_column, count):
        return [f'{filter_column}_{data_column}-{i}' for i in range(1, count+1)]
