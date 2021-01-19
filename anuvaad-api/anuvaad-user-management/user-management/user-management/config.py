import os
import time

#CROSS_MODULE_COMMON_CONFIGS
MONGO_SERVER_HOST = os.environ.get('MONGO_CLUSTER_URL', 'mongodb://localhost:27017,localhost:27018/?replicaSet=foo')#


#MODULE-SPECIFIC-CONFIGS

#module configs
DEBUG = False
CONTEXT_PATH = "/anuvaad/user-mgmt"
HOST = '0.0.0.0'
PORT = 5001
ENABLE_CORS = False

#mongodb-configs
MONGO_DB_HOST = os.environ.get('MONGO_IP', 'localhost')
MONGO_DB_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_DB_SCHEMA = os.environ.get('MONGO_DB_IDENTIFIER', 'usermanagement')
USR_MONGO_COLLECTION = os.environ.get('UMS_USR_COLLECTION', 'sample')
USR_TOKEN_MONGO_COLLECTION = os.environ.get( 'UMS_USR_TOKEN_COLLECTION', 'usertokens')
USR_TEMP_TOKEN_MONGO_COLLECTION = os.environ.get( 'UMS_USR_TEMP_TOKEN_COLLECTION', 'usertemptoken')
USR_ORG_MONGO_COLLECTION = os.environ.get('UMS_ORG_COLLECTION', 'organization')

#common-variables
MIN_LENGTH = os.environ.get('UMS_PASSWORD_MIN_LENGTH', 6)
OFFSET_VALUE=os.environ.get('UMS_OFFSET_VALUE', 0)
LIMIT_VALUE=os.environ.get('UMS_LIMIT_VALUE', 20)

#external file read configs
ROLE_CODES_URL = os.environ.get('UMS_ROLE_CODES_URL','https://raw.githubusercontent.com/project-anuvaad/anuvaad/zuul_gateway/anuvaad-api/anuvaad-zuul-api-gw/dev-configs/roles.json')
ROLE_CODES_DIR_PATH=os.environ.get('UMS_ROLE_DIR_PATH','/app/configs/') #'/home/jainy/Documents/Anuvaad_local_files/usrmgmt/'
ROLE_CODES_FILE_NAME=os.environ.get('UMS_FILE_NAME','roles.json')

#gmail server configs
MAIL_SETTINGS = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ.get('SUPPORT_EMAIL','XXXXX'),
    "MAIL_PASSWORD": os.environ.get('SUPPORT_EMAIL_PASSWORD','XX')}

# HREF_LINK=os.environ.get('MAIL_HREF_LINK','https://users.anuvaad.org')

BASE_URL=os.environ.get('REACT_APP_BASE_URL','https://developers.anuvaad.org/')