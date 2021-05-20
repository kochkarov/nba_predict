from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = ('game', 'member')
