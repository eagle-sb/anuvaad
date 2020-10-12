import os
import time

DEBUG = False
API_URL_PREFIX = "/anuvaad/user-mgmt/v1/users"
HOST = '0.0.0.0'
PORT = 5001

ENABLE_CORS = False

MONGO_DB_HOST   = os.environ.get('MONGO_IP', 'localhost')
MONGO_DB_PORT   = os.environ.get('MONGO_PORT', 27017)
MONGO_DB_SCHEMA = os.environ.get('MONGO_DB_IDENTIFIER', 'usermanagement')
