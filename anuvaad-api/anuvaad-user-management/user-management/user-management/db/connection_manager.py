from config import MONGO_SERVER_HOST
from config import MONGO_DB_SCHEMA
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
        print("**********Db connected")
        client = MongoClient(MONGO_SERVER_HOST)
        self.db = client[MONGO_DB_SCHEMA]
        return self.db

    def get_mongo_instance(self, collection):
        if not self.db:
            db_instance = self.instantiate()
        else:
            db_instance = self.db
        return db_instance[collection]

    


# class DbConnector:

#     def __init__(self):
#         pass

#     def instantiate(self):
#         client = pymongo.MongoClient(mongo_server_host)
#         db = client[mongo_translator_db]
#         return db

#     def get_mongo_instance(self, collection):
#         if not db:
#             db_instance = self.instantiate()
#         else:
#             db_instance = db
#         return db_instance[collection]

#     def create(self, object_in):
#             col = self.get_mongo_instance(mongo_translator_collection) 
#             col.insert_one(object_in)