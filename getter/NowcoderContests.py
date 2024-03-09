import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import json
from html import unescape

URL = 'https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=13'
JSON_FILE = 'events.json'

events_dict = {}

with open(JSON_FILE, 'r') as f:
    events_dict = json.load(f)
    events_sub_dict = events_dict['events']

web_text = requests.get(URL).text
datatable = BeautifulSoup(web_text, 'lxml').find_all('div', class_='platform-mod js-current')[0]
assert '等你来战' in datatable.text
contests = datatable.find_all('div', attrs={"data-id": True})
for contest in contests:
    inf_json = json.loads(unescape(contest.attrs['data-json']))
    # name
    name = inf_json['contestName']
    # uid
    uid = f'Nowcoder_{name}'
    # start time
    startTime = datetime.fromtimestamp(int(inf_json['contestStartTime']) / 1000) - timedelta(hours=8)
    # end time
    endTime = datetime.fromtimestamp(int(inf_json['contestEndTime']) / 1000) - timedelta(hours=8)
    sublink = contest.contents[1].contents[0].attrs['href']
    registerLink = f'https://ac.nowcoder.com{sublink}'
    events_sub_dict[uid] = {
        "uid": uid,
        "name": name,
        "now": datetime.now(pytz.utc).strftime('%Y%m%dT%H%M%SZ'),
        "startTime": startTime.strftime('%Y%m%dT%H%M%SZ'),
        "endTime": endTime.strftime('%Y%m%dT%H%M%SZ'),
        "url": registerLink,
        "description": registerLink
    }
    print(f'{name} has processed')

with open(JSON_FILE, 'w') as f:
    json.dump(events_dict, f, indent=4)
    
print(f'{len(contests)} contests found in Nowcoder')
