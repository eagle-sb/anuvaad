"""
 * @author ['aroop']
 * @email ['aroop.ghosh@tarento.com']
 * @create date 2020-05-28 12:40:01
 * @modify date 2020-05-28 12:40:01
 * @desc [description]
 """
from flask import Flask, jsonify, request
import os
import glob
from datetime import datetime
import time
import logging
import math
import json
import uuid
import multiprocessing as mp
from flask_cors import CORS
import flask as flask
import config
from model.response import CustomResponse
from model.status import Status
import magic

app = Flask(__name__)
# app.wsgi_app = LoggerMiddleware(app.wsgi_app)

CORS(app)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_FILE_TYPES = ['application/msword','application/pdf','image/x-ms-bmp','image/jpeg','image/jpg','image/png','text/plain','application/vnd.openxmlformats-officedocument.wordprocessingml.document']

log = logging.getLogger('file')

try:
    app_debug_logs = os.environ['app_debug_logs']

    if app_debug_logs == 'False':
        logging.disable(logging.DEBUG)
        log.info("DEBUG LOGS InACTIVE")
    else:
        log.info("DEBUG LOGS ACTIVE")
except:
    logging.disable(logging.DEBUG)
    log.info("DEBUG LOGS InACTIVE")


@app.route('/health', methods=['GET'])
def hello_():
    log.info('testing info log')
    log.info('testing debug logs')
    log.error('test error logs')
    return "hello"

@app.route('/anuvaad/v1/upload', methods=['POST'])
def upload_file():
    basename = str(int(time.time()))
    f = request.files['file']
    filetype = magic.from_buffer(f.read(), mime=True)
    filename = str(uuid.uuid4())+'_'+f.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], basename+'_'+filename)
    f.save(filepath)
    with open(filepath, 'rb') as f:
        filetype = magic.from_buffer(f.read(), mime=True)
        f.close()
        if filetype in ALLOWED_FILE_TYPES:
            res = CustomResponse(Status.SUCCESS.value, basename+'_'+f.filename)
            return res.getres()
        else:
            res = CustomResponse(Status.ERR_UNSUPPORTED_FILETYPE.value,None)
            return res.getres(), 400
    


@app.route('/anuvaad/v1/download', methods=['GET'])
def download_file():
    filename = request.args.get('file')
    if filename is None:
        res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value,None)
        return res.getres(), 400
    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'], filename)
    if(os.path.exists(filepath)):
        result = flask.send_file(filepath, as_attachment=True)
        result.headers["x-suggested-filename"] = filename
        return result
    else:
        res = CustomResponse(Status.DATA_NOT_FOUND.value,None)
        return res.getres(), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
