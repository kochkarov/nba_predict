#!/usr/bin/env python
import django
django.setup()
from services.api import ApiNba, set_code
from services.database import DataNba
from team.models import Team, Conference, Division
from game.models import Game

# Game.objects.all().delete()
# Team.objects.all().delete()
# Division.objects.all().delete()
# Conference.objects.all().delete()

apinba = ApiNba()
# apinba.create_teams()

# for year in range(2015, 2021):
#     apinba.update_data(year)
a = DataNba()
a.init_data(forced_call=True)
print(len(a.data.shape))
