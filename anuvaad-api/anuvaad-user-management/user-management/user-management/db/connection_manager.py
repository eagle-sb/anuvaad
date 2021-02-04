from config import MONGO_SERVER_HOST
from config import MONGO_DB_SCHEMA
from utilities import MODULE_CONTEXT
from pymongo import MongoClient
from anuvaad_auditor.loghandler import log_info, log_exception


# establishing connection with mongo instance
client = MongoClient(MONGO_SERVER_HOST)

def get_db():
    return client[MONGO_DB_SCHEMA]
    



class DbConnector:

    def __init__(self):
        self.db = None
        

    def instantiate(self):
        log_info("Establishing database connectivity",MODULE_CONTEXT)
        try:
            client = MongoClient(MONGO_SERVER_HOST)
            self.db = client[MONGO_DB_SCHEMA]
            return self.db
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)

    def get_mongo_instance(self, collection):
        if not self.db:
            db_instance = self.instantiate()
        else:
            db_instance = self.db
        return db_instance[collection]

    

