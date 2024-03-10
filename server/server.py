from flask import Flask, send_from_directory, make_response
import os

# command: gunicorn -w 8 -b ${IP}:${PORT} server:app --log-file=- --access-logfile=- --error-logfile=-

app = Flask(__name__)

FILES_DIRECTORY = '/home/ubuntu/ics-gen'

@app.route('/contests', methods=['GET'])
def get_contests():
    ics_file_path = os.path.join(FILES_DIRECTORY, "schedule.ics")
    response = make_response(send_from_directory(directory=os.path.dirname(ics_file_path), 
                                                 path=os.path.basename(ics_file_path), 
                                                 as_attachment=True))
    return response

@app.route('/contests_raw', methods=['GET'])
def get_contests_raw():
    ics_file_path = os.path.join(FILES_DIRECTORY, "events.json")
    response = make_response(send_from_directory(directory=os.path.dirname(ics_file_path), 
                                                 path=os.path.basename(ics_file_path)))
    return response