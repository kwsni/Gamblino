import io
import re
import time

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.images import ImageFile
from django.db import migrations


def sync_item_schema(apps, schema_editor):
        Case = apps.get_model('inventory', 'Case')
        Item = apps.get_model('inventory', 'Item')
        ItemPrice = apps.get_model('inventory', 'ItemPrice')

        item_schema = requests.get('https://bymykel.github.io/CSGO-API/api/en/crates.json').json()
        prices = requests.get('https://api.bitskins.com/market/skin/730').json()
        for c in item_schema:
            if c['type'] == 'Case':
                img = ImageFile(io.BytesIO(requests.get(c['image']).content), name=c['name'])
                time.sleep(1)
                case = Case.objects.create(
                    name=c['name'],
                    image=img
                )
                for i in c['contains']:
                    img = ImageFile(io.BytesIO(requests.get(i['image']).content), name=i['name'])
                    time.sleep(1)
                    item = Item.objects.create(
                        name=i['name'],
                        rarity=i['rarity']['name'],
                        image=img, 
                        case=case
                    )
                    for w in ['Factory New',
                            'Minimal Wear',
                            'Field-Tested',
                            'Well-Worn',
                            'Battle-Scarred']:
                        for s in [True, False]:
                            ItemPrice.objects.create(
                                item=item,
                                wear=w,
                                stattrak=s
                                )
                for i in c['contains_rare']:
                    img = ImageFile(io.BytesIO(requests.get(i['image']).content), name=i['name'])
                    time.sleep(1)
                    item, item_created = Item.objects.get_or_create(name=i['name'],
                        defaults={
                            'rarity': i['rarity']['name'],
                            'image': img, 
                            'case': case
                        }
                    )
                    if item_created:
                        for w in ['Factory New',
                                'Minimal Wear',
                                'Field-Tested',
                                'Well-Worn',
                                'Battle-Scarred']:
                            for s in [True, False]:
                                ItemPrice.objects.create(
                                    item=item,
                                    wear=w,
                                    stattrak=s
                                )
        for i in prices:
            regex = re.compile(r'(★ |)(StatTrak™ |)(.+) \((.+)\)')
            name = regex.search(i['name'])
            if name:
                try:
                    item = Item.objects.get(name=name.group(3))
                except ObjectDoesNotExist:
                    continue
                if item and i['suggested_price']:
                    ItemPrice.objects.update_or_create(item=item, wear=name.group(4), stattrak=False if name.group(2) == '' else True, 
                        defaults={
                            'item': item,
                            'wear': name.group(4),
                            'stattrak': bool(name.group(2)),
                            'price': float(i['suggested_price'] / 1000),
                        })

class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(sync_item_schema)
    ]