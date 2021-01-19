import uuid
from utilities import MODULE_CONTEXT
import config
from db import get_db
from anuvaad_auditor.loghandler import log_info, log_exception
from anuvaad_auditor.errorhandler import post_error



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
            collections = get_db()[config.USR_ORG_MONGO_COLLECTION]
            result = collections.find({"Code": orgCode}, {"_id": 0, "active": 1})
            log_info("searching for record with the recieved orgID:{}".format(result), MODULE_CONTEXT)
            if result.count() == 0:
                return post_error("Invalid Organization", "No such registered organization with the given code", None)
            for value in result:
                if value["active"] == False:
                    return post_error("Invalid Organization", "This Organization is currently inactive", None)

        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return post_error("Database connection exception", "An error occurred while connecting to the database:{}".format(str(e)), None)

    @staticmethod
    def validate_org_creation(org):
        if "code" not in org.keys():
            return post_error("Key error", "code not found", None)
        if "active" not in org.keys():
            return post_error("Key error", "active not found", None)
        if "description" not in org.keys():
            return post_error("Key error", "description not found", None)
            

        code = org["code"]
        active = org["active"]
        description = org["description"]
            

            
        if not code or not active or not description:
            return post_error("Data missing", "code,active,description", None)