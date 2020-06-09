from django.core.management.base import BaseCommand
from polls.models import Item
from django.utils import timezone
import datetime
from datetime import date


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Deleting...')
        d_now = datetime.datetime.now()
        for one_item in Item.objects.all():
            if one_item.paid == False and d_now > datetime.datetime(one_item.date_finish.year,one_item.date_finish.month,one_item.date_finish.day):
                    one_item.delete()
        print('Successfully deleted Items records!')
