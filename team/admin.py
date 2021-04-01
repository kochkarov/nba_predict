from django.contrib import admin
from .models import Team, Conference, Division


@admin.register(Team, Division, Conference)
class ReadOnlyAdmin(admin.ModelAdmin):
    # readonly_fields = ('all', 'the', 'necessary', 'fields')
    actions = None  # Removes the default delete action in list view

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
