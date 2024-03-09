import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import pytz
import json
from html import unescape
import re
from urllib.parse import unquote

URL = 'https://www.luogu.com.cn/contest/list'
JSON_FILE = 'events.json'

events_dict = {}

with open(JSON_FILE, 'r') as f:
    events_dict = json.load(f)
    events_sub_dict = events_dict['events']

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
headers = {
    'User-Agent': user_agent
}

web = requests.get(URL, headers=headers)
web_text = unquote(re.search(r'decodeURIComponent\((.*?)\)', web.text).group(1))[1:-1]
contests = json.loads(web_text)['currentData']['contests']['result']
now = datetime.now(timezone.utc)
count = 0
for contest in contests:
    # start time
    startTime = datetime.fromtimestamp(contest['startTime']) - timedelta(hours=8)
    startTime = startTime.replace(tzinfo=timezone.utc)
    if startTime < now:
        break
    # name
    name = contest['name']
    # uid
    uid = f'Luogu_{name}'
    # end time
    endTime = datetime.fromtimestamp(contest['endTime']) - timedelta(hours=8)
    contest_id = contest['id']
    registerLink = f'https://www.luogu.com.cn/contest/{str(contest_id)}'
    events_sub_dict[uid] = {
        "uid": uid,
        "name": name,
        "now": datetime.now(pytz.utc).strftime('%Y%m%dT%H%M%SZ'),
        "startTime": startTime.strftime('%Y%m%dT%H%M%SZ'),
        "endTime": endTime.strftime('%Y%m%dT%H%M%SZ'),
        "url": registerLink,
        "description": registerLink
    }
    count += 1
    print(f'{name} has processed')

with open(JSON_FILE, 'w') as f:
    json.dump(events_dict, f, indent=4)
    
print(f'{count} contests found in Luogu')
