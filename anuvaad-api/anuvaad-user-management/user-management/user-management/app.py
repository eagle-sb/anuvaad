from flask import Flask
from flask.blueprints import Blueprint
from flask_cors import CORS
from anuvaad_auditor.loghandler import log_info, log_exception
from anuvaad_auditor.errorhandler import post_error
import routes
import config
from utilities import MODULE_CONTEXT
import config
import requests
import json


role_codes_filepath = config.ROLE_CODES_URL
json_file_dir =  config.ROLE_CODES_DIR_PATH                               #"/home/jainy/Documents/usrmgmt/"
json_file_name = config.ROLE_CODES_FILE_NAME


def read_role_codes():
    try:
        file = requests.get(role_codes_filepath, allow_redirects=True)
        file_path = json_file_dir + json_file_name
        open(file_path, 'wb').write(file.content)
        with open(file_path, 'r') as stream:
            parsed = json.load(stream)
            roles = parsed['roles']
            rolecodes = []
            for role in roles:
                rolecodes.append(role["code"])
            return rolecodes
    except Exception as exc:
        log_exception("Exception while reading configs: " +
                      str(exc), None, exc)
        post_error("CONFIG_READ_ERROR",
                   "Exception while reading configs: " + str(exc), None)


# global ROLE_CODES
ROLE_CODES = read_role_codes()

server = Flask(__name__)

if config.ENABLE_CORS:
    cors = CORS(server, resources={r"/api/*": {"origins": "*"}})

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint, url_prefix=config.CONTEXT_PATH)

if __name__ == "__main__":
    log_info('starting server at {} at port {}'.format(
        config.HOST, config.PORT), MODULE_CONTEXT)
    server.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
