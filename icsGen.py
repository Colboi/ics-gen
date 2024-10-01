import os
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from eventsGetter.CodeforcesContests import Codeforces_contests
from eventsGetter.LeetCodeContests import LeetCode_contests
from eventsGetter.LuoguContests import Luogu_contests
from eventsGetter.NowcoderContests import Nowcoder_contests
from icalendar import Calendar, Event

# FILE SETTING
JSON_FILE = 'events.json'
ICS_FILE = 'schedule.ics'

# ALARM SETTING
ALARM = False
ALARM_TIME = '-PT0M'

# get json data
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w') as file:
        file.write('{}')
with open(JSON_FILE, 'r') as f:
    events = json.load(f)

# get web driver ready
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Edge(options=options)

events.update(Codeforces_contests())
events.update(LeetCode_contests(driver=driver))
events.update(Luogu_contests())
events.update(Nowcoder_contests())

with open(JSON_FILE, 'w') as f:
    json.dump(events, f, indent=4)

calendar = Calendar(creator='Colboi')
calendar.add('X-WR-TIMEZONE', 'Asia/Shanghai')
for uid, event_info in events.items():
    event = Event()
    event['uid'] = uid
    event['summary'] = event_info['name']
    event['dtstart'] = datetime.strptime(event_info['begin'], '%Y-%m-%dT%H:%M:%S').strftime('%Y%m%dT%H%M%S')
    event['dtend'] = datetime.strptime(event_info['end'], '%Y-%m-%dT%H:%M:%S').strftime('%Y%m%dT%H%M%S')
    event['description'] = event_info['description']
    event['url'] = event_info['url']

    calendar.add_component(event)

with open(ICS_FILE, 'wb') as f:
    f.write(calendar.to_ical())

# with open('schedule.ics', 'w', encoding='utf-8') as f:
#     f.write("""BEGIN:VCALENDAR
# VERSION:2.0
# CALSCALE:GREGORIAN
# PRODID:-//Colboi//OI Contests//CN
# METHOD:PUBLISH
# NAME:OI Contests
# X-WR-CALNAME:OI Contests
# DESCRIPTION:OI Contests / by Colboi
# X-WR-CALDESC:OI Contests / by Colboi
# X-WR-TIMEZONE:Asia/Shanghai
# """)
#     for event in data:
#         f.write(f"""BEGIN:VEVENT
# UID:{event[0]}
# SUMMARY:{event[1]}
# DTSTAMP:{event[2].strftime('%Y%m%dT%H%M%SZ')}
# DTSTART:{event[3].strftime('%Y%m%dT%H%M%SZ')}
# DTEND:{event[4].strftime('%Y%m%dT%H%M%SZ')}
# STATUS:CONFIRMED
# URL:{event[5]}
# DESCRIPTION:{event[6]}
# BEGIN:VALARM
# TRIGGER:-PT0M
# END:VALARM
# END:VEVENT
# """)
#         print(f'{event[1]} is generated')
#     f.write('END:VCALENDAR')

driver.quit()
# TODO - logging finish