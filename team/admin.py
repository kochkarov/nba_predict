from django.contrib import admin
from .models import Team, Conference, Division
# Register your models here.

admin.site.register(Conference)
admin.site.register(Division)
admin.site.register(Team)
