import requests, requests, re

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from inventory.models import Case, Item

class Command(BaseCommand):
    help = 'Updates item and case prices'

    def handle(self, *args, **options):
        prices = requests.get('https://api.bitskins.com/market/skin/730').json()
        gamblino_api = 'http://192.168.0.154:8000/api/v1'

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