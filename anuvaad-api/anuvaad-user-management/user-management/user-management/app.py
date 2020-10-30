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
json_file_dir = config.ROLE_CODES_DIR_PATH  # "/home/jainy/Documents/usrmgmt/"
json_file_name = config.ROLE_CODES_FILE_NAME
ROLE_CODES=[]

server = Flask(__name__)

def read_role_codes():
    with server.test_request_context():
        try:
            file = requests.get(role_codes_filepath, allow_redirects=True)
            file_path = json_file_dir + json_file_name
            open(file_path, 'wb').write(file.content)
            log_info("data read from git and pushed to local", MODULE_CONTEXT)
            with open(file_path, 'r') as stream:
                parsed = json.load(stream)
                roles = parsed['roles']
                log_info("roles read from json are {}".format(
                    roles), MODULE_CONTEXT)
                rolecodes = []
                for role in roles:
                    if role["active"]:
                        rolecodes.append(role["code"])
                        log_info(
                    "rolecodes read from json is stored on to rolecodes array:{} ".format(rolecodes), MODULE_CONTEXT)
            ROLE_CODES=rolecodes
        except Exception as exc:
            log_exception("Exception while reading configs: " +
                        str(exc), MODULE_CONTEXT, exc)
            post_error("CONFIG_READ_ERROR",
                    "Exception while reading configs: " + str(exc), MODULE_CONTEXT)


# global ROLE_CODES




if config.ENABLE_CORS:
    cors = CORS(server, resources={r"/api/*": {"origins": "*"}})

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint, url_prefix=config.CONTEXT_PATH)

if __name__ == "__main__":
    log_info('starting server at {} at port {}'.format(
        config.HOST, config.PORT), MODULE_CONTEXT)
    read_role_codes()
    server.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
