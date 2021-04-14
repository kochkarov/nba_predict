from services.database import DataNba
from sklearn.linear_model import LogisticRegression


class Predictor(DataNba):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.seasons = []
        self.mask = ''
        self.X_train = None
        self.y_train = None
        self.X_predict = None
        self.y_predict = None
        self.model = None

    def fit(self):
        pass

    def predict(self, x):
        self.X_predict = x
        self.y_predict = self.model.predict(self.X_predict)
        return self.y_predict

    def get_data(self):
        df = self.data[self.data.season.isin(self.seasons) & (self.data.is_home_game == 1)]
        self.X_train = df[self.get_columns(self.mask)]
        self.y_train = df.is_win
        return


class SimplePredictor(Predictor):
    def __init__(self, seasons: list, mask: str):
        super().__init__()
        self.seasons = seasons
        self.mask = mask
        self.name = f'Team OneHot {self.seasons}'

    def fit(self):
        self.get_data()
        self.model = LogisticRegression(random_state=13).fit(self.X_train, self.y_train)

    def get_x(self):
        self.X_predict = self.data[(self.data.season == 2020) &
                                   (self.data.is_home_game == 1)][self.get_columns(self.mask)]
        return self.X_predict

    def get_y(self):
        return self.data.is_win[(self.data.season == 2020) & (self.data.is_home_game == 1)]

    def score(self):
        self.fit()
        self.predict(self.get_x())
        return self.model.score(self.X_predict, self.get_y())
