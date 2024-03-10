import os
import json

# if events.json doesn't exist, generate it

JSON_FILE = 'events.json'

if os.path.exists(JSON_FILE):
    print(f'{JSON_FILE} already exists')
else:
    with open(JSON_FILE, 'w') as f:
        json.dump({"events": {}}, f, indent=4)
    print('finished init')
