import json
import os

JSON_FILE = 'events.json'

events = None
with open(JSON_FILE, 'r') as f:
    events = json.load(f)['events']

with open('event.ics', 'w', encoding='utf-8') as f:
    f.write("""BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
PRODID:-//Colboi//ACM Contests//CN
METHOD:PUBLISH
NAME:ACM Contests
X-WR-CALNAME:ACM Contests
DESCRIPTION:ACM Contests / by Colboi
X-WR-CALDESC:ACM Contests / by Colboi
X-WR-TIMEZONE:Asia/Shanghai
""")
    for event_name in events:
        event = events[event_name]
        f.write(f"""BEGIN:VEVENT
UID:{event['uid']}
SUMMARY:{event['name']}
DTSTAMP:{event['now']}
DTSTART:{event['startTime']}
DTEND:{event['endTime']}
STATUS:CONFIRMED
URL:{event['url']}
DESCRIPTION:{event['description']}
END:VEVENT
""")
        print(f'{event_name} is generated')
    f.write('END:VCALENDAR')
print('finished')