from django.contrib import admin
from .models import Prediction
# Register your models here.


@admin.register(Prediction)
class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = ('game', 'member', 'game_date')
