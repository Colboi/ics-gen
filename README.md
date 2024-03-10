# .ics Generator

by Colboi

# Usage

1. `pip selenium ...` *[WIP]*

2. modifiy prefix of ics file in `icsGen.py` (such as `NAME`, `X-WR-TIMEZONE`)

3. modify `bash run.sh` as you wish

4. run `bash run.sh`

# Customization for eventsGetter

Each eventsGetter will read `events.json` and modify `events`' value then save file.

- make sure all *eventsGetter*s are python scripts.

- each event should include keys and values below:

  - `uid` -> `UID`: Unique identifier of the event (e.g. siteName_eventName).

  - `name` -> `SUMMARY`: Name of the event.

  - `now` -> `DTSTAMP`: Current time stamp in format: `%Y%m%dT%H%M%SZ`. Note that time zone is **UTC**.

  - `startTime` -> `DTSTART`: Start time stamp. Same format as above.

  - `endTime` -> `DTEND`: End time stamp. Same format as above.
  
  - `url` -> `URL`: URL of the event.

  - `description` -> `DESCRIPTION`: Description of the event.

# Tips

- You can create your own script referring to examples in `eventsGetter` folder.

  *These examples provide several OI contests' schedule. You can give it a try.*

- You can use it in conjunction with *crontab*.

- You can create your own *Flask* server referring to the example in `server` folder.
