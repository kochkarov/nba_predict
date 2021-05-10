from services.database import DataNba
# from sklearn.linear_model import LogisticRegression
import xgboost as xgb
import numpy as np
import pandas as pd


class Bot(DataNba):
    def __init__(self, param: dict):
        super().__init__()
        self.param = param
        self.X_train = None
        self.y_train = None
        self.X_predict = None
        self.y_predict = None
        self.y_true = None
        self.model = None

    def fit(self):
        pass

    def predict(self, x):
        return self.model.predict(x)

    def get_data(self, seasons: list, real_predict=0):
        if real_predict:
            df = self.data[self.data.season.isin(seasons) & (self.data.is_home_game == 1) &
                           self.data.is_win.isna()]
        else:
            df = self.data[self.data.season.isin(seasons) & (self.data.is_home_game == 1) &
                           self.data.is_win.notna()]

        x = df[self.get_column_names(self.param['mask'])].dropna()
        y = df.is_win.loc[x.index]
        return x, y

    @classmethod
    def score(cls, predict, true, prn=0):
        eq = np.sum(predict == true)
        total = len(true)
        if prn:
            print(f'{eq*100/total:.2f} %    {eq} of {total}')
        return eq / total


# class SimplePredictor(Predictor):
#     def __init__(self, seasons: list, mask: str):
#         super().__init__()
#         self.seasons = seasons
#         self.mask = mask
#         self.name = f'Team OneHot {self.seasons}'
#
#     def fit(self):
#         self.get_data()
#         self.model = LogisticRegression(random_state=13).fit(self.X_train, self.y_train)
#
#     def get_x(self):
#         self.X_predict = self.data[(self.data.season == 2020) &
#                                    (self.data.is_home_game == 1)][self.get_columns(self.mask)]
#         return self.X_predict
#
#     def get_y(self):
#         return self.data.is_win.loc[self.X_predict.index]
#
#     def score(self):
#         self.fit()
#         self.predict(self.get_x())
#         return self.model.score(self.X_predict, self.get_y())


class XgbBot(Bot):
    def __init__(self, param: dict):
        super().__init__(param)
        self.param.setdefault('seasons', list(range(2015, 2020)))
        self.param.setdefault('count', 20)
        self.param.setdefault('mask', ['_diff_', '_is_win-'])
        self.param.setdefault('objective', 'binary:hinge')
        self.param.setdefault('num_boost_round', 100)
        self.param.setdefault('verbosity', 0)
        self.name = f'XGB, use last {self.param["count"]} results'

    def fit(self):
        self.X_train, self.y_train = self.get_data(self.param['seasons'])
        self.model = xgb.train(self.param, xgb.DMatrix(self.X_train, label=self.y_train),
                               num_boost_round=self.param['num_boost_round'])

        # self.data['ypredict'] = self.model.predict(xgb.DMatrix(self.data[self.features]))

    def determination(self):
        base_score = self.score(np.ones(len(self.y_true)), self.y_true)
        this_score = self.score(self.y_predict, self.y_true)
        return (this_score - base_score) / (1 - base_score)

    def rate_prediction(self):
        self.fit()
        self.X_predict, self.y_true = self.get_data([2020])
        self.y_predict = self.predict(xgb.DMatrix(self.X_predict))
        return self.determination()

    def make_predict(self):
        self.fit()
        self.X_predict, self.y_true = self.get_data([2020], True)
        self.y_predict = self.predict(xgb.DMatrix(self.X_predict))
        return self.data.loc[self.X_predict.index][['date', 'human']].assign(predict=self.y_predict.astype(int))

    def check_date_predict(self, date: str):
        self.fit()
        df = self.data[(self.data.date == pd.Timestamp(date)) & (self.data.is_home_game == 1) &
                       self.data.is_win.notna()]

        self.X_predict = df[self.get_column_names(self.param['mask'])].dropna()
        self.y_true = df.is_win.loc[self.X_predict.index]
        self.y_predict = self.predict(xgb.DMatrix(self.X_predict)).astype(int)
        self.score(self.y_predict, self.y_true, 1)
        res = self.data.loc[self.X_predict.index][['date', 'human', 'is_win']].assign(predict=self.y_predict)
        res.is_win = res.is_win.astype(int)
        return res
