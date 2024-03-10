import json
from datetime import datetime

JSON_FILE = 'events.json'

events = None
with open(JSON_FILE, 'r') as f:
    events = json.load(f)['events']

print("current time:", datetime.now())

with open('schedule.ics', 'w', encoding='utf-8') as f:
    f.write("""BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
PRODID:-//Colboi//OI Contests//CN
METHOD:PUBLISH
NAME:OI Contests
X-WR-CALNAME:OI Contests
DESCRIPTION:OI Contests / by Colboi
X-WR-CALDESC:OI Contests / by Colboi
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