from bs4 import BeautifulSoup
from datetime import datetime
import logging
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

URL = 'https://leetcode.cn/contest/'

def LeetCode_contests(driver) -> dict:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    driver.get(URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '添加到日程表')]")))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    contests = soup.find_all('div', class_='contest-card-base')
    assert len(contests) > 0

    events = {}

    # weekly

    inf = contests[0].contents[0].contents[0].contents[1].contents
    # name
    name = inf[2].contents[0]
    contest_id = name.split(' ')[1]
    # uid
    uid = f'LeetCode_{contest_id}'
    # start time & end time
    timestr = inf[4].contents[0]
    # if isinstance(timestr, str):
    start_time_match = re.search(r'(\d{4}-\d{2}-\d{2})：(\d{2}:\d{2})', timestr)
    end_time_match = re.search(r'(\d{2}:\d{2}) ~ (\d{2}:\d{2})', timestr)
    assert start_time_match and end_time_match
    start_date_str, start_time_str = start_time_match.groups()
    end_time_str = end_time_match.group(2)
    startTime = datetime.strptime(start_date_str + ' ' + start_time_str, '%Y-%m-%d %H:%M')
    endTime = datetime.strptime(start_date_str + ' ' + end_time_str, '%Y-%m-%d %H:%M')
    subLink = contests[0].contents[0].contents[0].attrs['href']
    # else:
    #     timestr = inf[3].contents[1].contents[0].split('~')
    #     startTime = datetime.strptime(timestr[0], '%Y-%m-%d / %H:%M ').replace(tzinfo=timezone(timedelta(hours=8)))
    #     endTime = datetime.strptime(timestr[1], ' %Y-%m-%d / %H:%M').replace(tzinfo=timezone(timedelta(hours=8)))
    #     subLink = contests[0].contents[0].attrs['href']

    events[f'Leetcode_{contest_id}'] = {
        "name": name,
        "begin": startTime.strftime('%Y-%m-%dT%H:%M:%S'),
        "end": endTime.strftime('%Y-%m-%dT%H:%M:%S'),
        "url": f'https://leetcode.cn{subLink}',
        "description": f'https://leetcode.cn{subLink}'
    }
    
    logging.info(f'{name} has processed')

    # biweekly

    inf = contests[1].contents[0].contents[0].contents[1].contents
    # name
    name = inf[1].contents[0]
    contest_id = name.split(' ')[1]
    # start time & end time
    timestr = inf[3].contents[1].contents[0].split('~')
    startTime = datetime.strptime(timestr[0], '%Y-%m-%d / %H:%M ')
    endTime = datetime.strptime(timestr[1], ' %Y-%m-%d / %H:%M')
    subLink = contests[1].contents[0].attrs['href']

    events[f'Leetcode_{contest_id}'] = {
        "name": name,
        "begin": startTime.strftime('%Y-%m-%dT%H:%M:%S'),
        "end": endTime.strftime('%Y-%m-%dT%H:%M:%S'),
        "url": f'https://leetcode.cn{subLink}',
        "description": f'https://leetcode.cn{subLink}'
    }

    logging.info(f'{name} has processed')
    logging.info(f'{len(contests)} contests found in LeetCode')
    
    return events

if __name__ == '__main__':
    LeetCode_contests()