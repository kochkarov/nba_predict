import pandas as pd
from sklearn.linear_model import LogisticRegression
from scipy import stats
from services.database import DataNba
import xgboost as xgb
import numpy as np


class Bot(DataNba):
    def __init__(self, param: dict):
        super().__init__()
        self.param = param
        self.param.setdefault('num_boost_round', 100)
        self.param.setdefault('seasons', list(range(2015, 2020)))
        self.param.setdefault('mask', ['_oh_'])
        self.columns = self.get_column_names(self.param['mask'])
        self.model = None
        self.y_predict = None
        self.y_true = None

    def fit(self):
        pass

    def predict(self, x):
        return self.model.predict(x)

    def id_to_index(self, game_list: list[str]):
        return self.data[(self.data.game_id.isin(game_list)) & (self.data.is_home_game == 1)].index

    def make_predict(self, game_list: list[str]):
        """
        Сделать прогноз на игры из списка game_list
        :param game_list: список идентификаторов игр (параметр game_id из модели Game)
        :return:
        """
        pass

    def get_data(self, seasons: list[int]):
        x = self.data[self.data.season.isin(seasons) & (self.data.is_home_game == 1)][self.columns].dropna()
        y = self.data.is_win.loc[x.index]
        return x, y

    @classmethod
    def score(cls, predict, true, prn=0):
        eq = np.sum(predict == true)
        total = len(true)
        if prn:
            print(f'{eq*100/total:.2f} %    {eq} of {total}')
        return eq / total


class AlwaysWinBot(Bot):
    def make_predict(self, game_list: list[str]):
        return [{'game_id': game_id, 'predict': 1} for game_id in game_list]


class AlwaysLoseBot(Bot):
    def make_predict(self, game_list: list[str]):
        return [{'game_id': game_id, 'predict': 0} for game_id in game_list]


class RandomBot(Bot):
    def make_predict(self, game_list: list[str]):
        predict_list = np.random.randint(2, size=len(game_list))
        return [{'game_id': game_id, 'predict': predict} for game_id, predict in zip(game_list, predict_list)]


class LogisticBot(Bot):
    def __init__(self, param: dict):
        super().__init__(param)
        self.param.setdefault('mask', ['_diff_'])
        self.param.setdefault('count', 20)
        self.param.setdefault('class_weight', None)

    def fit(self):
        self.init_data()
        x_train, y_train = self.get_data(self.param['seasons'])
        norm = pd.DataFrame(stats.zscore(x_train.values, axis=0), columns=x_train.columns)
        self.model = LogisticRegression(random_state=0, class_weight=self.param['class_weight']).fit(norm, y_train)

    def make_predict(self, game_list: list[str]):
        super().make_predict(game_list)
        idx = self.id_to_index(game_list)
        self.fit()

        x = self.data.loc[idx][self.get_column_names(self.param['mask'])].dropna()
        y = self.predict(x).astype(int)

        return [{'game_id': game_id, 'predict': predict}
                for game_id, predict in zip(x.index.get_level_values('game_id'), y)]


class XgbBot(Bot):
    def __init__(self, param: dict):
        super().__init__(param)
        self.param.setdefault('count', 20)
        self.param.setdefault('mask', ['_diff_', '_is_win-'])
        self.param.setdefault('objective', 'binary:hinge')
        self.param.setdefault('verbosity', 0)
        self.name = f'XGB, use last {self.param["count"]} results'

    def fit(self):
        self.init_data()
        x_train, y_train = self.get_data(self.param['seasons'])
        self.model = xgb.train(self.param, xgb.DMatrix(x_train, label=y_train),
                               num_boost_round=self.param['num_boost_round'])

    def determination(self):
        base_score = self.score(np.ones(len(self.y_true)), self.y_true)
        this_score = self.score(self.y_predict, self.y_true)
        return (this_score - base_score) / (1 - base_score)

    def rate_prediction(self):
        self.fit()
        x, self.y_true = self.get_data([2020])
        self.y_predict = self.predict(xgb.DMatrix(x))
        return self.determination()

    def make_predict(self, game_list: list[str]):
        super().make_predict(game_list)
        idx = self.id_to_index(game_list)
        self.fit()

        x = self.data.loc[idx][self.get_column_names(self.param['mask'])].dropna()
        y = self.predict(xgb.DMatrix(x)).astype(int)

        return [{'game_id': game_id, 'predict': predict}
                for game_id, predict in zip(x.index.get_level_values('game_id'), y)]
