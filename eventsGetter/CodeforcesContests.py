import requests
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import os

SH_TZ = ZoneInfo("Asia/Shanghai")

def get_codeforces_contests(json_file: str):
    url = "https://codeforces.com/api/contest.list"
    response = requests.get(url, timeout=10)
    codeforces_contests = json.loads(response.text)['result']

    if os.path.exists(json_file):
        contests = json.loads(open(json_file, "r").read())
    else:
        contests = {}
    
    for cfcontest in codeforces_contests:
        contest_id = f'codeforces_{cfcontest["id"]}'
        contests[contest_id] = {}
        # contests[contest_id]['id'] = cfcontest['id']
        contests[contest_id]['summary'] = cfcontest['name']
        contests[contest_id]['description'] = f'{cfcontest["type"]} scoring system'
        contests[contest_id]['dtstart'] = datetime.fromtimestamp(cfcontest['startTimeSeconds'], tz=SH_TZ).isoformat()
        contests[contest_id]['dtend'] = datetime.fromtimestamp(cfcontest['startTimeSeconds'] + cfcontest['durationSeconds'], tz=SH_TZ).isoformat()
        contests[contest_id]['url'] = f'https://codeforces.com/contest/{cfcontest["id"]}'
    json.dump(contests, open(json_file, "w"), indent=4)

if __name__ == "__main__":
    get_codeforces_contests('json/CodeforcesContests.json')