#!/usr/bin/env python3
import django
django.setup()
from api.service import ApiNba

apinba = ApiNba()
apinba.add_teams()
