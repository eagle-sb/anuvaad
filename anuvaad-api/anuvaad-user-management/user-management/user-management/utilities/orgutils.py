import uuid
from utilities import MODULE_CONTEXT
from config import USR_ORG_MONGO_COLLECTION, USR_MONGO_COLLECTION
from db import DbConnector
from db import get_db
from anuvaad_auditor.loghandler import log_info, log_exception
from anuvaad_auditor.errorhandler import post_error


connector=DbConnector()
class OrgUtils:

    def __init__(self):
        pass
#orgId generation
    @staticmethod
    def generate_org_id():
        return(uuid.uuid4().hex)

    @staticmethod
    def validate_org(orgCode):
        try:
            collections = connector.get_mongo_instance(USR_ORG_MONGO_COLLECTION)
            result = collections.find({"code": orgCode}, {"_id": 0, "active": 1})
            log_info("searching for record with the recieved orgID:{}".format(result), MODULE_CONTEXT)
            if result.count() == 0:
                return post_error("Invalid Organization", "No such registered organization with the given Org Id", None)
            for value in result:
                if value["active"] == False:
                    return post_error("Invalid Organization", "Organization is currently inactive", None)

        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return post_error("Database connection exception", "An error occurred while connecting to the database:{}".format(str(e)), None)

    @staticmethod
    def validate_org_upsert(i,org):
        if "code" not in org.keys():
            return post_error("Key error", "code not found", None)
        if "active" not in org.keys():
            return post_error("Key error", "active not found", None)
        code = str(org["code"]).upper()
        active = org["active"]
            
        if not code:
            return post_error("Data missing", "code is mandatory field this cannot be null for record {}".format(str(i+1)), None)
        if active==None:
            return post_error("Data missing", "active status is mandatory that cannot be null for record {}".format(str(i+1)), None)
        if active == False:
            try:
                collections = connector.get_mongo_instance(USR_MONGO_COLLECTION)
                result = collections.find({"orgID": code,"is_active":True})
                if result.count()!=0:
                    log_info("Deactivation request for org failed, {} active users with the orgID".format(str(result.count())), MODULE_CONTEXT)
                    return post_error("Deactivation Failed","There exist active users in {} hence this action cannot be performed".format(code),None)

            except Exception as e:
                log_exception("db connection exception ",  MODULE_CONTEXT, e)
                return post_error("Database connection exception", "An error occurred while connecting to the database:{}".format(str(e)), None)