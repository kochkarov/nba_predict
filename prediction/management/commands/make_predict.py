from django.core.management.base import BaseCommand
from services.api import ApiNba


class Command(BaseCommand):
    help = 'Update games data from NBA'

    def handle(self, *args, **options):
        print('Update starting...')
        ApiNba().update_data()
