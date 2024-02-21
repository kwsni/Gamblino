from random import randint, choice
from requests import get
from urllib.parse import urljoin
from json import loads

class Loot:
    def __init__(self):
        self._cs2_api = 'https://bymykel.github.io/CSGO-API/api/en/'  # Full JSON list API
        self.id = "crate-4001"                                        # temporarily hardcoded to 'CS:GO Weapon Case'
        self.loot = ""
        self.rarity = ""
        self.name = ""
        self.img = ""
        self.stattrak = False
        self.wear = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
    
    def uncrate(self):
        cases = get(urljoin(self._cs2_api, "crates.json")).text
        case = [c for c in loads(cases) if c["id"] == self.id]
        # Based on published odds: https://www.csgo.com.cn/news/gamebroad/20170911/206155.shtml
        rng = randint(1,782)
        # Rare (Gold)
        if(rng <= 2):
            self.rarity = "Rare"
            self.loot = choice(case[0]["contains_rare"])
        # Covert (Red)
        elif(rng <= 7):
            self.rarity = "Covert"
            self.loot = choice([x for x in case[0]["contains"] if x['rarity']['name'] == "Covert"])
        # Classified (Pink)
        elif(rng <= 32):
            self.rarity = "Classified"
            self.loot = choice([x for x in case[0]["contains"] if x['rarity']['name'] == "Classified"])
        # Restricted (Purple)
        elif(rng <= 157):
            self.rarity = "Restricted"
            self.loot = choice([x for x in case[0]["contains"] if x['rarity']['name'] == "Restricted"])
        # Mil-Spec (Blue)
        else:
            self.rarity = "Mil-Spec Grade"
            self.loot = choice([x for x in case[0]["contains"] if x['rarity']['name'] == "Mil-Spec Grade"])
        self.name = self.loot["name"]
        self.img = self.loot["image"]

        # Determine StatTrak™
        rng = randint(1,10)
        if(rng == 1):
            self.stattrak = True

        # Determine wear
        rng = randint(0,4)
        self.wear = self.wear[rng]

        return self

    def __str__(self):
        stattrak_str = lambda : "StatTrak™ " if self.stattrak else ""
        return f"{self.wear}{stattrak_str()}{self.name}"
