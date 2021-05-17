#!/usr/bin/env python
import django
django.setup()

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
    Member.objects.update_or_create(name='Всезнайка 5', is_bot=1, defaults={'param': param})

    param = {'class_name': 'XgbBot', 'seasons': [2015, 2016, 2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_', '_is_win-']}
    Member.objects.update_or_create(name='Умник 5', is_bot=1, defaults={'param': param})

    param = {'class_name': 'XgbBot', 'seasons': [2015, 2016, 2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_']}
    Member.objects.update_or_create(name='Мудрый 5', is_bot=1, defaults={'param': param})

    param = {'class_name': 'XgbBot', 'seasons': [2017, 2018, 2019], 'count': 20,
             'mask': ['_diff_']}
    Member.objects.update_or_create(name='Мудрый 3', is_bot=1, defaults={'param': param})

    param = {'class_name': 'XgbBot', 'seasons': [2015, 2016, 2017, 2018, 2019], 'count': 20,
             'mask': ['_oh_']}
    Member.objects.update_or_create(name='Новичок 5', is_bot=1, defaults={'param': param})

    param = {'class_name': 'XgbBot', 'seasons': [2017, 2018, 2019], 'count': 20,
             'mask': ['_oh_']}
    Member.objects.update_or_create(name='Новичок 3', is_bot=1, defaults={'param': param})

    param = {'class_name': 'XgbBot', 'seasons': [2019], 'count': 20,
             'mask': ['_oh_']}
    Member.objects.update_or_create(name='Новичок 1', is_bot=1, defaults={'param': param})

    param = {'class_name': 'BaseBot'}
    Member.objects.update_or_create(name='Dumb', is_bot=1, defaults={'param': param})


if __name__ == '__main__':
    create_bots()
