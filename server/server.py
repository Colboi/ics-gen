from flask import Flask, send_from_directory, make_response
import os

# 运行命令: gunicorn -w 8 -b ${IP}:${PORT} server:app --log-file=- --access-logfile=- --error-logfile=-

app = Flask(__name__)

FILES_DIRECTORY = '/home/ubuntu/ics-gen'

#响应mpd文件
@app.route('/contests', methods=['GET'])
def get_mpd():
    ics_file_path = os.path.join(FILES_DIRECTORY, "event.ics")
    response = make_response(send_from_directory(directory=os.path.dirname(ics_file_path), 
                                                 path=os.path.basename(ics_file_path), 
                                                 as_attachment=True))
    return response
