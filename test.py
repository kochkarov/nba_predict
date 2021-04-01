#!/usr/bin/env python
import django
django.setup()
from api.service import ApiNba, set_code
from team.models import Team, Conference, Division
from game.models import Game

apinba = ApiNba()
# apinba.create_teams()
# set_code(Division)
# set_code(Conference)
# set_code(Team)


# Game.objects.all().delete()
# Team.objects.all().delete()
# Division.objects.all().delete()
# Conference.objects.all().delete()

for year in range(2015, 2021):
    apinba.get_and_save_games(year)
