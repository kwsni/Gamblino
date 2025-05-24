import re
from os import getenv

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from inventory.models import Case, Item

load_dotenv(override=True)

class Command(BaseCommand):
    help = 'Updates item and case prices'

    def handle(self, *args, **options):
        prices = requests.get('https://api.bitskins.com/market/skin/730').json()
        gamblino_api = f'{getenv('DJANGO_API_URL')}/api/v1'

        print('Starting price update')
        for p in prices:
            regex = re.compile(r'(★ |)(StatTrak™ |)(.+) \((.+)\)')
            name = regex.search(p['name'])
            if name:
                try:
                    item = Item.objects.get(name=name.group(3))
                except ObjectDoesNotExist:
                    try:
                        case = Case.objects.get(name=name.group(5))
                    except ObjectDoesNotExist:
                        continue
                if p['suggested_price']:
                    data = {'price': float(p['suggested_price'] / 1000)}
                else:
                    continue
                if item:
                    requests.patch(f"{gamblino_api}/item/{name.group(3)}/{name.group(4)}{f'''{'/stattrak' if not name.group(2) else ''}'''}/price", json=data)
                elif case:
                    requests.patch(f"{gamblino_api}/case/{name.group(5)}/price", json=data)
        print('Finished price update')