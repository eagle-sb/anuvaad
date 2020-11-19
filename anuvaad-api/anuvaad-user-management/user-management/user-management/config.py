import os
import time

DEBUG = False
CONTEXT_PATH = "/anuvaad/user-mgmt"
# API_URL_PREFIX = "/v1/users"
HOST = '0.0.0.0'
PORT = 5001

ENABLE_CORS = False

MONGO_DB_HOST = os.environ.get('MONGO_IP', 'localhost')
MONGO_DB_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_DB_SCHEMA = os.environ.get('MONGO_DB_IDENTIFIER', 'usermanagement')

USR_MONGO_COLLECTION = os.environ.get('UMS_USR_COLLECTION', 'sample')
USR_TOKEN_MONGO_COLLECTION = os.environ.get(
    'UMS_USR_TOKEN_COLLECTION', 'usertokens')

MIN_LENGTH = os.environ.get('UMS_PASSWORD_MIN_LENGTH', 6)

ROLE_CODES_URL = os.environ.get('UMS_ROLE_CODES_URL','https://raw.githubusercontent.com/project-anuvaad/anuvaad/zuul_gateway/anuvaad-api/anuvaad-zuul-api-gw/dev-configs/roles.json')

ROLE_CODES_DIR_PATH=os.environ.get('UMS_ROLE_DIR_PATH','/app/configs/') #'/home/jainy/Documents/usrmgmt/'

ROLE_CODES_FILE_NAME=os.environ.get('UMS_FILE_NAME','roles.json')

MAIL_SETTINGS = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ.get('EMAIL_USER','xxxxx@xxxxx.com'),
    "MAIL_PASSWORD": os.environ.get('EMAIL_PASSWORD','aaxxx')

}

HREF_LINK=os.environ.get('MAIL_HREF_LINK','https://users.anuvaad.org')