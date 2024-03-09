from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import json
import re
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

URL = 'https://leetcode.cn/contest/'
JSON_FILE = 'events.json'

events_dict = {}

with open(JSON_FILE, 'r') as f:
    events_dict = json.load(f)
    events_sub_dict = events_dict['events']

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
# options.add_argument('--remote-debugging-port=10000')

driver = webdriver.Edge(options=options)
driver.get(URL)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '添加到日程表')]")))

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
contests = soup.find_all('div', class_='contest-card-base')
assert len(contests) > 0

# weekly

inf = contests[0].contents[0].contents[0].contents[1].contents
# name
name = inf[2].contents[0]
# uid
uid = f'LeetCode_{name}'
# start time & end time
timestr = inf[4].contents[0]
if isinstance(timestr, str):
    start_time_match = re.search(r'(\d{4}-\d{2}-\d{2})：(\d{2}:\d{2})', timestr)
    end_time_match = re.search(r'(\d{2}:\d{2}) ~ (\d{2}:\d{2})', timestr)
    assert start_time_match and end_time_match
    start_date_str, start_time_str = start_time_match.groups()
    end_time_str = end_time_match.group(2)
    startTime = datetime.strptime(start_date_str + ' ' + start_time_str, '%Y-%m-%d %H:%M') - timedelta(hours=8)
    endTime = datetime.strptime(start_date_str + ' ' + end_time_str, '%Y-%m-%d %H:%M') - timedelta(hours=8)
    subLink = contests[0].contents[0].contents[0].attrs['href']
else:
    timestr = inf[3].contents[1].contents[0].split('~')
    startTime = datetime.strptime(timestr[0], '%Y-%m-%d / %H:%M ') - timedelta(hours=8)
    endTime = datetime.strptime(timestr[1], ' %Y-%m-%d / %H:%M') - timedelta(hours=8)
    subLink = contests[0].contents[0].attrs['href']
    
registerLink = f'https://leetcode.cn{subLink}'
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

# biweekly

inf = contests[1].contents[0].contents[0].contents[1].contents
# name
name = inf[1].contents[0]
# uid
uid = f'LeetCode_{name}'
# start time & end time
timestr = inf[3].contents[1].contents[0].split('~')
startTime = datetime.strptime(timestr[0], '%Y-%m-%d / %H:%M ') - timedelta(hours=8)
endTime = datetime.strptime(timestr[1], ' %Y-%m-%d / %H:%M') - timedelta(hours=8)
subLink = contests[1].contents[0].attrs['href']

registerLink = f'https://leetcode.cn{subLink}'
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
    
print(f'{len(contests)} contests found in LeetCode')
