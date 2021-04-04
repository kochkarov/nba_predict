#!/usr/bin/env python
import django
django.setup()
from services.api import ApiNba, set_code
from team.models import Team, Conference, Division
from game.models import Game

apinba = ApiNba()
# apinba.create_teams()


# Game.objects.all().delete()
# Team.objects.all().delete()
# Division.objects.all().delete()
# Conference.objects.all().delete()

# for year in range(2015, 2021):
#     apinba.get_and_save_games(year)
