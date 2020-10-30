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




server = Flask(__name__)




# global ROLE_CODES




if config.ENABLE_CORS:
    cors = CORS(server, resources={r"/api/*": {"origins": "*"}})

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint, url_prefix=config.CONTEXT_PATH)

if __name__ == "__main__":
    log_info('starting server at {} at port {}'.format(
        config.HOST, config.PORT), MODULE_CONTEXT)
    server.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
