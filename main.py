#!/usr/bin/env python
import django
django.setup()

from championship.models import Championship, Score, Prediction, Event, League
from services.moderator import Moderator
from member.models import Member
from services.api import ApiNba
from services.database import DataNba
from team.models import Team, Conference, Division
from game.models import Game


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
            champ, _ = Championship.objects.get_or_create(name=f'{event.__str__()} {league.name}',
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


def create_bots():
    param = {'class_name': 'XgbBot', 'seasons': [2015, 2016, 2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_', '_is_win-', '_oh_']}
    Member.objects.update_or_create(name='Dif win oh 5', is_bot=1, defaults={'param': param})

    param = {'class_name': 'XgbBot', 'seasons': [2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_', '_is_win-', '_oh_']}
    Member.objects.update_or_create(name='Dif win oh 3', is_bot=1, defaults={'param': param})

    param = {'class_name': 'XgbBot', 'seasons': [2015, 2016, 2017, 2018, 2019], 'count': 20,
             'mask': ['_is_win-']}
    Member.objects.update_or_create(name='Win 5', is_bot=1, defaults={'param': param})

    param = {'class_name': 'XgbBot', 'seasons': [2017, 2018, 2019], 'count': 20,
             'mask': ['_is_win-']}
    Member.objects.update_or_create(name='Win 3', is_bot=1, defaults={'param': param})

    param = {'class_name': 'XgbBot', 'seasons': [2015, 2016, 2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_']}
    Member.objects.update_or_create(name='Dif 5', is_bot=1, defaults={'param': param})

    param = {'class_name': 'XgbBot', 'seasons': [2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_']}
    Member.objects.update_or_create(name='Dif 3', is_bot=1, defaults={'param': param})

    param = {'class_name': 'XgbBot', 'seasons': [2015, 2016, 2017, 2018, 2019], 'count': 20,
             'mask': ['_oh_']}
    Member.objects.update_or_create(name='Oh 5', is_bot=1, defaults={'param': param})

    param = {'class_name': 'XgbBot', 'seasons': [2017, 2018, 2019], 'count': 20,
             'mask': ['_oh_']}
    Member.objects.update_or_create(name='Oh 3', is_bot=1, defaults={'param': param})

    param = {'class_name': 'XgbBot', 'seasons': [2019], 'count': 20,
             'mask': ['_oh_']}
    Member.objects.update_or_create(name='Oh 1', is_bot=1, defaults={'param': param})

    param = {'class_name': 'AlwaysWinBot', 'mask': ['_oh_']}
    Member.objects.update_or_create(name='Dumb', is_bot=1, defaults={'param': param})

    param = {'class_name': 'AlwaysLoseBot', 'mask': ['_oh_']}
    Member.objects.update_or_create(name='Dumber', is_bot=1, defaults={'param': param})

    param = {'class_name': 'RandomBot', 'mask': ['_oh_']}
    Member.objects.update_or_create(name='Crazy', is_bot=1, defaults={'param': param})


if __name__ == '__main__':
    create_championships()
    # champ = Championship.objects.get(name='Test championship')
    # moder = Moderator(champ)
    # moder.make_prediction()
    # moder.calc_result()
