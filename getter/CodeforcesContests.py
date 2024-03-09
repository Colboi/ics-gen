import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import json

URL = 'https://codeforces.com/contests?complete=true'
JSON_FILE = 'events.json'

contest_dict = {}

with open(JSON_FILE, 'r') as f:
    contest_dict = json.load(f)
    events_dict = contest_dict['events']

web_text = requests.get(URL).text
datatable = BeautifulSoup(web_text, 'lxml').find_all('div', class_='datatable')[0]
assert 'Current or upcoming contests' in datatable.text
contests = datatable.find_all('tr', attrs={"data-contestid": True})
for contest in contests:
    infs = contest.find_all('td')
    # name
    name = infs[0].contents[0].strip()
    # uid
    uid = f'Codeforce_{name}'
    # start time
    startTime = datetime.strptime(infs[2].contents[1].contents[1].contents[0], '%b/%d/%Y %H:%M') - timedelta(hours=3)
    # duration
    duration_str = infs[3].contents[0].strip()
    duration = timedelta(hours=int(duration_str.split(':')[0]), minutes=int(duration_str.split(':')[1]))
    # end time
    endTime = startTime + duration
    sublink = infs[5].contents[1].attrs['href']
    registerLink = f'https://codeforces.com{sublink}'
    events_dict[uid] = {
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
    json.dump(contest_dict, f, indent=4)

print(f'{len(contests)} contests found in Codeforces')