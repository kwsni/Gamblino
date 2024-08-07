import logging
from typing_extensions import Self
from random import randint, choice
from aiohttp_client_cache.session import CachedSession
from aiohttp_client_cache import SQLiteBackend
from urllib.parse import urljoin

log = logging.getLogger(__name__)

class Loot:
    def __init__(self) -> None:
        self._cs2_api = 'https://bymykel.github.io/CSGO-API/api/en/'  # Full JSON list API
        self.containers = []
        self.container = {}
        self.loot = ''
        self.rarity = ''
        self.name = ''
        self.img = ''
        self.stattrak = False
        self.wear = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']

    async def get(self, container: str) -> list[dict]:
        async with CachedSession(cache=SQLiteBackend(expire_after=60*60)) as session:
            async with session.get(urljoin(self._cs2_api, 'crates.json')) as r:
                self.containers = await r.json()
        return [c for c in self.containers if c['type'] == container]
    
    async def rollCase(self, container_name: str) -> Self:
        cases = await self.get('Case')
        if(container_name is not ''):
            for c in cases:
                if c['name'] == container_name:
                    self.container = c
                    break
        else:
            self.container = choice(cases)
        # Based on published odds: https://www.csgo.com.cn/news/gamebroad/20170911/206155.shtml
        rng = randint(1,782)
        # Rare (Gold)
        if(rng <= 2):
            self.rarity = 'Rare'
            self.loot = choice(self.container['contains_rare'])
        # Covert (Red)
        elif(rng <= 7):
            self.rarity = 'Covert'
            self.loot = choice([x for x in self.container['contains'] if x['rarity']['name'] == 'Covert'])
        # Classified (Pink)
        elif(rng <= 32):
            self.rarity = 'Classified'
            self.loot = choice([x for x in self.container['contains'] if x['rarity']['name'] == 'Classified'])
        # Restricted (Purple)
        elif(rng <= 157):
            self.rarity = 'Restricted'
            self.loot = choice([x for x in self.container['contains'] if x['rarity']['name'] == 'Restricted'])
        # Mil-Spec (Blue)
        else:
            self.rarity = 'Mil-Spec Grade'
            self.loot = choice([x for x in self.container['contains'] if x['rarity']['name'] == 'Mil-Spec Grade'])
        self.name = self.loot['name']
        self.img = self.loot['image']

        # Determine StatTrak™
        rng = randint(1,10)
        if(rng == 1):
            self.stattrak = True

        # Determine wear
        rng = randint(0,4)
        self.wear = self.wear[rng]

        return self

    def __str__(self) -> str:
        stattrak_str = lambda : 'StatTrak™ ' if self.stattrak else ''
        return f'{self.wear}{stattrak_str()}{self.name}'
