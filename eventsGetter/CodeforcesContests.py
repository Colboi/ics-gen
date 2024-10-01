import requests
import logging
from datetime import datetime, timedelta
import json

def Codeforces_contests() -> dict:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    URL = 'https://codeforces.com/api/contest.list'

    contests = json.loads(requests.get(URL).text)['result']
    
    events = {}

    for contest in contests:
        # 2024-10-13T00:00:00+08:00
        begin_time = datetime.fromtimestamp(contest['startTimeSeconds'])
        events[f'Codeforces_{contest["id"]}'] = {
            "name": contest['name'],
            "begin": begin_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "end": (begin_time + timedelta(seconds=contest['durationSeconds'])).strftime('%Y-%m-%dT%H:%M:%S'),
            "url": f'https://codeforces.com/contest/{contest["id"]}',
            "description": f'https://codeforces.com/contest/{contest["id"]}'
        }
    
    return events

if __name__ == '__main__':
    Codeforces_contests()