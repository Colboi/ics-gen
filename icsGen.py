import os
import json
import yaml
from datetime import datetime
from icalendar import Calendar, Event, vText
from pathlib import Path

# ALARM SETTING
ALARM = False
ALARM_TIME = '-PT0M'

def ics_gen(prodid: str = "-//Colboi//Calendar Export//CN", ALARM=None):
    """
    ALARM: None / '-PT0M' / '-PT10M' / '-PT30M' / '-PT1H' / '-P1D'
    """
    enabled_getters = []
    with open('config.yaml', 'r', encoding='utf-8') as f:
        enabled_getters = yaml.safe_load(f).get('enable_getters', [])
    
    # check output dirs
    if not os.path.exists('json'):
        os.makedirs('json')
    if not os.path.exists('ics'):
        os.makedirs('ics')

    for getter in enabled_getters:
        os.system(f'python3 eventsGetter/{getter}.py')
        
        cal = Calendar()
        cal.add("prodid", prodid)
        cal.add("version", "2.0")
        cal.add("calscale", "GREGORIAN")
        cal.add("method", "PUBLISH")
        cal.add("X-WR-CALNAME", f'{getter}')
        
        events = json.loads(open(f'json/{getter}.json', 'r').read())

        for uid, item in events.items():
            ve = Event()
            ve.add("uid", uid)
            if "summary" in item:     ve.add("summary", vText(str(item["summary"])))
            if "description" in item: ve.add("description", vText(str(item["description"])))
            if "url" in item:         ve.add("url", vText(str(item["url"])))
            ve.add("dtstart", datetime.fromisoformat(item["dtstart"]))
            ve.add("dtend", datetime.fromisoformat(item["dtend"]))

            cal.add_component(ve)

        out_path = Path(f'ics/{getter}.ics')
        out_path.write_bytes(cal.to_ical())

    # for uid, event_info in events.items():
    #     event = Event()
    #     event['uid'] = uid
    #     event['summary'] = event_info['name']
    #     event['dtstart'] = datetime.strptime(event_info['begin'], '%Y-%m-%dT%H:%M:%S').strftime('%Y%m%dT%H%M%S')
    #     event['dtend'] = datetime.strptime(event_info['end'], '%Y-%m-%dT%H:%M:%S').strftime('%Y%m%dT%H%M%S')
    #     event['description'] = event_info['description']
    #     event['url'] = event_info['url']

    #     calendar.add_component(event)

    # with open(ICS_FILE, 'wb') as f:
    #     f.write(calendar.to_ical())

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

if __name__ == '__main__':
    ics_gen()