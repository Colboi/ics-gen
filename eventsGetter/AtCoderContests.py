import os
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
from urllib.parse import urljoin
from zoneinfo import ZoneInfo
import re

SH_TZ = ZoneInfo("Asia/Shanghai")

def AtCoder_beginner_contests(json_file: str, url='https://atcoder.jp/contests/'):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if os.path.exists(json_file):
        contests = json.loads(open(json_file, "r").read())
    else:
        contests = {}

    web_text = requests.get(url, timeout=10).text
    datatable = BeautifulSoup(web_text, 'lxml').find_all('table', class_='table table-default table-striped table-hover table-condensed table-bordered small')[1]
    contest_infs = datatable.find_all('tbody')[0].find_all('tr')
    
    cnt = 0
    for contest in contest_infs:
        tds = contest.find_all("td")
        
        # check class
        if "user-blue" not in tds[1].find_all("span")[1].get("class", []):
            continue
        
        # time
        time_text = tds[0].find("time").text
        dtstart = datetime.strptime(time_text, '%Y-%m-%d %H:%M:%S%z')
        dtstart = dtstart.astimezone(SH_TZ)
        h, m = map(int, tds[2].get_text(strip=True).split(':'))
        delta = timedelta(hours=h, minutes=m)
        dtend = dtstart + delta
        
        # summary
        title = tds[1].text.split('\n')[-2]
        # match "AtCoder Beginner Contest %d"
        m = re.search(r'AtCoder Beginner Contest (\d+)', title)
        summary = m.group(0)
        uid = summary.replace(' ', '_')
        
        # url
        a = tds[1].find("a", href=True)
        contest_url = urljoin(url, a["href"]) if a else None
        
        # description
        description = f'{title}, Rated range: {tds[3].text.strip()}'
        
        contests[uid] = {
            "summary": summary,
            "dtstart": dtstart.isoformat(),
            "dtend": dtend.isoformat(),
            "url": contest_url,
            "description": description
        }
        
        cnt += 1
        logging.info(f'{summary} has processed')

    logging.info(f'{cnt} contests found in Atcoder')

    json.dump(contests, open(json_file, 'w'), indent=4)

if __name__ == '__main__':
    AtCoder_beginner_contests('json/AtCoderContests.json')
