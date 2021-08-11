import pandas as pd
from django.db import models
from django.contrib.auth.models import User
from sklearn.linear_model import LogisticRegression
from tqdm.auto import tqdm

from championship.models import Prediction
from services.bot import XgbBot, Bot, AlwaysWinBot, AlwaysLoseBot, RandomBot, LogisticBot
from services.bot import NaiveBayesBot, KNeighborsBot, SVCBot, DecisionTreeBot


class Human(User):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Member(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('User name', max_length=64, default='')
    is_bot = models.IntegerField(verbose_name='Bot signature', default=1)
    human = models.ForeignKey('Human', related_name='+', on_delete=models.PROTECT,
                              verbose_name='Human user', default=None, null=True)
    param = models.JSONField(null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = None

    def __str__(self):
        if self.is_bot:
            return f"Bot {self.name} {self.param['class_name']}"
        return f'{self.name}'

    def restore_bot(self):
        if self.is_bot:
            cls = globals()[self.param['class_name']]
            self.bot = cls(self.param)

    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Боты'


class StackBot(LogisticBot):
    stack_bots = ['DecisionTree-3', 'KNeighbors-5', 'LogReg-5', 'NaiveBayes-3', 'SVC-3', 'XGBoost-5']

    def fit(self):
        self.init_data()

        _, stack_train = self.get_data(self.param['seasons'])
        stack_train.index = stack_train.index.droplevel()
        stack_train = pd.DataFrame(stack_train).astype(int)
        stack_train.columns = ['ytrue']
        game_list = stack_train.index

        bot_dict = {}
        for predictor in tqdm(Member.objects.filter(is_bot=1), desc='StackBot training...'):
            predictor.restore_bot()
            if predictor.name in self.stack_bots:
                predictor.bot.fit()
                bot_dict[predictor.name] = predictor
                df = pd.DataFrame.from_dict(predictor.bot.make_predict(game_list))
                df = df.set_index('game_id')
                df.columns = [predictor.name]
                stack_train = stack_train.join(df)

        self.model = LogisticRegression(random_state=0, class_weight=self.param['class_weight']).fit(
            stack_train[self.stack_bots], stack_train['ytrue'])

    def make_predict(self, game_list: list[str]):
        data = Prediction.objects.filter(game__game_id__in=game_list, member__name__in=self.stack_bots
                                         ).values_list('game__game_id', 'member__name', 'predict')
        df = pd.DataFrame(index=game_list, columns=self.stack_bots)
        for game_id, name, predict in data:
            df.at[game_id, name] = predict
        y = self.predict(df).astype(int)
        return [{'game_id': game_id, 'predict': predict} for game_id, predict in zip(df.index, y)]


class EnsembleBot(LogisticBot):
    ensemble_bots = ['KNeighbors-5', 'LogReg-5', 'SVC-5']

    # ensemble_bots = ['KNeighbors-3', 'KNeighbors-5', 'LogReg-3', 'LogReg-5',
    #                  'SVC-3', 'SVC-5', 'XGBoost-5', 'NaiveBayes-3', 'DecisionTree-3']
    # ensemble_bots = ['DecisionTree-3', 'DecisionTree-5', 'KNeighbors-3', 'KNeighbors-5', 'LogReg-3', 'LogReg-5',
    #                  'NaiveBayes-3', 'NaiveBayes-5', 'SVC-3', 'SVC-5', 'XGBoost-3', 'XGBoost-5']

    def fit(self):
        pass

    def make_predict(self, game_list: list[str]):
        data = Prediction.objects.filter(game__game_id__in=game_list, member__name__in=self.ensemble_bots
                                         ).values_list('game__game_id', 'member__name', 'predict')
        df = pd.DataFrame(index=game_list, columns=self.ensemble_bots)
        for game_id, name, predict in data:
            df.at[game_id, name] = predict
        y = (df.mean(axis=1) + 0.5) // 1
        return [{'game_id': game_id, 'predict': int(predict)} for game_id, predict in zip(df.index, y)]
