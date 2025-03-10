import logging
from util.loot import Loot
import aiohttp, asyncio

log = logging.getLogger(__name__)

class TestOpen():
    def __init__(self, case_name: str) -> None:
        self.case_name = case_name

    async def case(self) -> None:
        loot = await Loot().rollCase(self.case_name)
        print(loot)
        loot_json = {'uid': 1, 'username': 'Tester', 'item': loot.name, 'wear': loot.wear, 'rarity': loot.rarity}
        auth = {'X-API-Key': 'some0key'}
        async with aiohttp.ClientSession('http://192.168.0.154:8000/') as session:
            async with session.post('/api/open-case', json=loot_json) as response:
                api_r = await response.json()
                #TODO: cond: send msg when api confirmed
                print(api_r)

t = TestOpen("Chroma Case")
asyncio.run(t.case())