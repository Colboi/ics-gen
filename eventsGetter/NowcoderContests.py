import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime
import json
from html import unescape

URL = 'https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=13'

def Nowcoder_contests() -> dict:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    web_text = requests.get(URL).text
    datatable = BeautifulSoup(web_text, 'lxml').find_all('div', class_='platform-mod js-current')[0]
    assert '等你来战' in datatable.text
    contests = datatable.find_all('div', attrs={"data-id": True})
    
    events = {}
    for contest in contests:
        inf_json = json.loads(unescape(contest.attrs['data-json']))
        # name
        name = inf_json['contestName']
        # uid
        uid = f'Nowcoder_{name}'
        # start time
        startTime = datetime.fromtimestamp(int(inf_json['contestStartTime']) / 1000)
        # end time
        endTime = datetime.fromtimestamp(int(inf_json['contestEndTime']) / 1000)
        
        events[f'Nowcoder_{inf_json["contestId"]}'] = {
            "name": inf_json['contestName'],
            "begin": startTime.strftime('%Y-%m-%dT%H:%M:%S'),
            "end": endTime.strftime('%Y-%m-%dT%H:%M:%S'),
            "url": f'https://ac.nowcoder.com{contest.contents[1].contents[0].attrs["href"]}',
            "description": f'https://ac.nowcoder.com{contest.contents[1].contents[0].attrs["href"]}'
        }
        logging.info(f'{name} has processed')

    logging.info(f'{len(contests)} contests found in Nowcoder')
    
    return events

if __name__ == '__main__':
    Nowcoder_contests()
