from flask import Flask, send_from_directory, make_response
import os

# command: gunicorn -w 8 -b ${IP}:${PORT} server:app --log-file=- --access-logfile=- --error-logfile=-

app = Flask(__name__)

FILES_DIRECTORY = 'ics'

# @app.route('/contests', methods=['GET'])
# def get_contests():
#     ics_file_path = os.path.join(FILES_DIRECTORY, "contests.ics")
#     response = make_response(send_from_directory(directory=os.path.dirname(ics_file_path), 
#                                                  path=os.path.basename(ics_file_path), 
#                                                  as_attachment=True))
#     return response

@app.route('/CodeforcesContests', methods=['GET'])
def get_codeforces_contests():
    ics_file_path = os.path.join(FILES_DIRECTORY, "CodeforcesContests.ics")
    response = make_response(send_from_directory(directory=os.path.dirname(ics_file_path), 
                                                 path=os.path.basename(ics_file_path), 
                                                 as_attachment=True))
    return response

@app.route('/LeetCodeContests', methods=['GET'])
def get_leetcode_contests():
    ics_file_path = os.path.join(FILES_DIRECTORY, "LeetCodeContests.ics")
    response = make_response(send_from_directory(directory=os.path.dirname(ics_file_path), 
                                                 path=os.path.basename(ics_file_path), 
                                                 as_attachment=True))
    return response

@app.route('/LuoguContests', methods=['GET'])
def get_luogu_contests():
    ics_file_path = os.path.join(FILES_DIRECTORY, "LuoguContests.ics")
    response = make_response(send_from_directory(directory=os.path.dirname(ics_file_path), 
                                                 path=os.path.basename(ics_file_path), 
                                                 as_attachment=True))
    return response

@app.route('/NowcoderContests', methods=['GET'])
def get_nowcoder_contests():
    ics_file_path = os.path.join(FILES_DIRECTORY, "NowcoderContests.ics")
    response = make_response(send_from_directory(directory=os.path.dirname(ics_file_path), 
                                                 path=os.path.basename(ics_file_path), 
                                                 as_attachment=True))
    return response

@app.route('/eoe', methods=['GET'])
def get_eoe_schedule():
    ics_file_path = os.path.join(FILES_DIRECTORY, "eoe.ics")
    response = make_response(send_from_directory(directory=os.path.dirname(ics_file_path), 
                                                 path=os.path.basename(ics_file_path)))
    return response

@app.route('/AtCoderContests', methods=['GET'])
def get_atcoder_schedule():
    ics_file_path = os.path.join(FILES_DIRECTORY, "AtCoderContests.ics")
    response = make_response(send_from_directory(directory=os.path.dirname(ics_file_path), 
                                                 path=os.path.basename(ics_file_path)))
    return response

@app.route('/contests_raw', methods=['GET'])
def get_contests_raw():
    ics_file_path = os.path.join(FILES_DIRECTORY, "contests.json")
    response = make_response(send_from_directory(directory=os.path.dirname(ics_file_path), 
                                                 path=os.path.basename(ics_file_path)))
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)