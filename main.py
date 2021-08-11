#!/usr/bin/env python
import django
django.setup()

from championship.models import Championship, Score, Prediction, Event, League
from services.moderator import Moderator
from member.models import Member, StackBot, EnsembleBot
from services.api import ApiNba
from services.database import DataNba
from team.models import Team, Conference, Division
from game.models import Game
from tqdm.auto import tqdm
from django.db.models import Max, Min, F


def delete_games():
    Game.objects.all().delete()
    Team.objects.all().delete()
    Division.objects.all().delete()
    Conference.objects.all().delete()


def create_championships():
    leagues = League.objects.all()
    events = Event.objects.all()
    for event in events:
        for league in leagues:
            agg = event.games.all().aggregate(date_min=Min('game_date'), date_max=Max('game_date'))
            name = f'{agg["date_min"]} - {agg["date_max"]} ({len(event.games.all())} games)'
            champ, _ = Championship.objects.get_or_create(name=name,
                                                          league=league, event=event)


def delete_championships():
    Score.objects.all().delete()
    Prediction.objects.all().delete()
    Championship.objects.all().delete()
    # Event.objects.all().delete()


def create_teams():
    apinba = ApiNba()
    apinba.create_teams()


def create_games():
    apinba = ApiNba()
    for year in range(2015, 2021):
        apinba.update_data(year)


def predict_all():
    Score.objects.all().delete()
    Prediction.objects.all().delete()
    Member.objects.all().delete()
    create_bots()
    league = League.objects.get(name='Rusanovka')
    league.members.add(*Member.objects.all())
    # create_championships()
    Moderator.make_all_prediction()
    for champ in tqdm(Championship.objects.all(), desc='Rating calculation...'):
        Moderator(champ).calc_result()


def create_bots():

    param = {'class_name': 'XgbBot', 'seasons': [2015, 2016, 2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_'], 'num_parallel_tree': 2, 'num_boost_round': 200, 'max_depth': 7}
    Member.objects.update_or_create(name='XGBoost-5', is_bot=1, defaults={'param': param})
    param['seasons'] = [2017, 2018, 2019]
    Member.objects.update_or_create(name='XGBoost-3', is_bot=1, defaults={'param': param})

    param = {'class_name': 'AlwaysWinBot', 'mask': ['_oh_']}
    Member.objects.update_or_create(name='ConstantWin', is_bot=1, defaults={'param': param})

    param = {'class_name': 'AlwaysLoseBot', 'mask': ['_oh_']}
    Member.objects.update_or_create(name='ConstantLose', is_bot=1, defaults={'param': param})

    # param = {'class_name': 'RandomBot', 'mask': ['_oh_']}
    # Member.objects.update_or_create(name='Random', is_bot=1, defaults={'param': param})

    param = {'class_name': 'LogisticBot', 'seasons': [2015, 2016, 2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_'], 'class_weight': 'balanced'}
    Member.objects.update_or_create(name='LogReg-5', is_bot=1, defaults={'param': param})
    param['seasons'] = [2017, 2018, 2019]
    Member.objects.update_or_create(name='LogReg-3', is_bot=1, defaults={'param': param})

    param = {'class_name': 'KNeighborsBot', 'seasons': [2015, 2016, 2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_'], 'class_weight': 'balanced', 'neighbors': 51}
    Member.objects.update_or_create(name='KNeighbors-5', is_bot=1, defaults={'param': param})
    param['seasons'] = [2017, 2018, 2019]
    param['neighbors'] = 67
    Member.objects.update_or_create(name='KNeighbors-3', is_bot=1, defaults={'param': param})

    param = {'class_name': 'SVCBot', 'seasons': [2015, 2016, 2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_'], 'class_weight': 'balanced'}
    Member.objects.update_or_create(name='SVC-5', is_bot=1, defaults={'param': param})
    param['seasons'] = [2017, 2018, 2019]
    Member.objects.update_or_create(name='SVC-3', is_bot=1, defaults={'param': param})

    param = {'class_name': 'NaiveBayesBot', 'seasons': [2015, 2016, 2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_'], 'class_weight': 'balanced'}
    Member.objects.update_or_create(name='NaiveBayes-5', is_bot=1, defaults={'param': param})
    param['seasons'] = [2017, 2018, 2019]
    Member.objects.update_or_create(name='NaiveBayes-3', is_bot=1, defaults={'param': param})

    param = {'class_name': 'DecisionTreeBot', 'seasons': [2015, 2016, 2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_'], 'class_weight': 'balanced'}
    Member.objects.update_or_create(name='DecisionTree-5', is_bot=1, defaults={'param': param})
    param['seasons'] = [2017, 2018, 2019]
    Member.objects.update_or_create(name='DecisionTree-3', is_bot=1, defaults={'param': param})

    param = {'class_name': 'StackBot', 'seasons': [2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_'], 'class_weight': 'balanced'}
    Member.objects.update_or_create(name='Stacking', is_bot=2, defaults={'param': param})

    param = {'class_name': 'EnsembleBot', 'seasons': [2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_'], 'class_weight': 'balanced'}
    Member.objects.update_or_create(name='Ensemble', is_bot=2, defaults={'param': param})


if __name__ == '__main__':
    predict_all()
    # Moderator.make_all_prediction(['EnsembleBot'])
    # for champ in tqdm(Championship.objects.all(), desc='Rating calculation...'):
    #     Moderator(champ).calc_result()
