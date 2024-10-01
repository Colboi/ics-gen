import requests
import logging
from datetime import datetime
import json
import re
from urllib.parse import unquote

URL = 'https://www.luogu.com.cn/contest/list'

# REQUESTS SETTING
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def Luogu_contests() -> dict:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    web = requests.get(URL, headers=HEADERS)
    web_text = unquote(re.search(r'decodeURIComponent\((.*?)\)', web.text).group(1))[1:-1]
    contests = json.loads(web_text)['currentData']['contests']['result']
    now = datetime.now()
    count = 0
    
    events = {}
    for contest in contests:
        # start time
        startTime = datetime.fromtimestamp(contest['startTime'])
        if startTime < now:
            break
        # end time
        endTime = datetime.fromtimestamp(contest['endTime'])
        events[f'Luogu_{contest["id"]}'] = {
            "name": contest['name'],
            "begin": startTime.strftime('%Y-%m-%dT%H:%M:%S'),
            "end": endTime.strftime('%Y-%m-%dT%H:%M:%S'),
            "url": f'https://www.luogu.com.cn/contest/{contest["id"]}',
            "description": f'https://www.luogu.com.cn/contest/{contest["id"]}'
        }
        count += 1
        logging.info(f'{contest["name"]} has processed')

    logging.info(f'{count} contests found in Luogu')
    
    return events

if __name__ == '__main__':
    Luogu_contests()