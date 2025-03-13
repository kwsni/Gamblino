import requests

from django.core.management.base import BaseCommand, CommandError

from inventory.models import Case, Item, ItemWear

class Command(BaseCommand):
    help = 'Updates the database to the latest item schema'

    def handle(self, *args, **options):
        item_schema = requests.get('https://bymykel.github.io/CSGO-API/api/en/crates.json').json()
        #TODO: Include market prices
        for c in item_schema:
            case, case_created = Case.objects.get_or_create(name=c['name'],
                defaults={
                    'name': c['name'],
                    'image': c['image']
                })
            if case_created:
                self.stdout.write(self.style.SUCCESS(f'Added {case.name} to database'))
            for i in c['contains']:
                item, item_created = Item.objects.get_or_create(name=i['name'],
                    defaults={
                        'name': i['name'],
                        'rarity': i['rarity']['name'],
                        'image': i['image'], 
                        'case': case
                    }
                )
                if item_created:
                        self.stdout.write(self.style.SUCCESS(f'Added {item.name} to database'))
                for w in ['Factory New',
                          'Minimal Wear',
                          'Field-Tested',
                          'Well-Worn',
                          'Battle-Scarred']:
                    iw, iw_created = ItemWear.objects.get_or_create(item=item, wear=w,
                        defaults={
                            'item': item,
                            'wear': w,
                        }
                    )
                    if iw_created:
                        self.stdout.write(self.style.SUCCESS(f'Added {iw.wear} {iw.item.name} to database'))
