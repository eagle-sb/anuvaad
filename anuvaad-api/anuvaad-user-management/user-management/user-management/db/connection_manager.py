import config
from pymongo import MongoClient
from anuvaad_auditor.loghandler import log_info, log_exception
from utilities import MODULE_CONTEXT

#establishing connection with mongo instance
client = MongoClient(config.MONGO_SERVER_HOST)

def get_db():
    return client[config.MONGO_DB_SCHEMA]
