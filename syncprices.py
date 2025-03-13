# Rate limit:
# 20/min
# 1000/day
# 500 min/day (8 hours 20 min / day) minimum @ 1 request/3 secs

import sys, time, json, requests

with open('items.json', 'r') as items_json, open('cases.json', 'r') as cases_json:
    print('Starting item and case price update')
    market_api = 'https://steamcommunity.com/market/priceoverview/?appid=730&market_hash_name='
    gamblino_api = 'http://192.168.0.154:8000/api/v1'

    items = json.load(items_json)
    cases = json.load(cases_json)

    total = len(cases) + len(items)
    
    i_ratio = len(items) / total
    c_ratio = len(cases) / total

    i_limit = int(1000 * i_ratio)
    c_limit = int(1000 * c_ratio)

    print('Starting item price update')
    for i in items[:i_limit]:
        url = market_api + f"{i['name']} ({i['wear']})"
        r = requests.get(url)
        data = {'price': r.json().get('median_price', '0.03'), 'wear': i['wear']}
        data['price'] = data['price'][1:] 
        requests.patch(gamblino_api + f"/item/{i['name']}/{i['wear']}/price", json=data)
        time.sleep(3)
    print('Finished item price update')

    print('Starting case price update')
    for c in cases[:c_limit]:
        r = requests.get(market_api + c['name'])
        data = {'price': r.json().get('median_price', '0.03')}
        data['price'] = data['price'][1:]
        requests.patch(gamblino_api + f"/case/{i['name']}/price", json=data)
        time.sleep(3)
    print('Finished case price update')

print('Finished item and case price update')

with open('items.json', 'w') as items_json:
    json.dump(items[i_limit:], items_json, indent=2)
print('Updated items.json')

with open('cases.json', 'w') as cases_json:
    json.dump(cases[c_limit:], cases_json, indent=2)
print('Updated cases.json')