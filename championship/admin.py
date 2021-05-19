from django.contrib import admin

from .models import Championship, League

admin.site.register(League)


@admin.register(Championship)
class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = ('games', 'members', 'predictions')
