from utilities import MODULE_CONTEXT
from db import get_db
from utilities import OrgUtils
from anuvaad_auditor.loghandler import log_info, log_exception
from anuvaad_auditor.errorhandler import post_error
import config
import pymongo


class UserOrganizationModel(object):

    def __init__(self):
        collections = get_db()[config.USR_ORG_MONGO_COLLECTION]
        try:
            collections.create_index('code', unique = True)
        except pymongo.errors.DuplicateKeyError as e:
            log_info("duplicate key, ignoring",MODULE_CONTEXT)
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)

    @staticmethod
    def create_organizations(orgs):
        try:
            collections = get_db()[config.USR_ORG_MONGO_COLLECTION]
        
            for org in orgs:
                org_data = {}
                code=str(org["code"]).upper()
                orgId =OrgUtils.generate_org_id()

                org_data['orgID'] = orgId
                org_data['active'] = org["active"]
                org_data['description'] = org["description"]
                
                collections.update({'code': code},{'$set': org_data},upsert=True)
        except pymongo.errors.WriteError as e:
            log_info("some of the record has duplicates ",  MODULE_CONTEXT)
            log_exception("update organization: exception ",  MODULE_CONTEXT, e)
        
        except Exception as e:
            log_exception("db connection exception " +
                          str(e),  MODULE_CONTEXT, e)
            return post_error("Database  exception", "An error occurred while processing on the db :{}".format(str(e)), None)


    @staticmethod
    def get_orgs_by_keys(org_code):
        

        exclude = {"_id":False}

        try:
            collections = get_db()[config.USR_ORG_MONGO_COLLECTION]
            if org_code== None :
                out = collections.find({"active":True},exclude)
                record_count=out.count()
            else:
                out = collections.find({"code":str(org_code).upper()}, exclude)
                log_info("org search is executed:{}".format(out), MODULE_CONTEXT)
                record_count=out.count()

            result = []
            for record in out:
                result.append(record)
            if not result:
                return None
            return result,record_count

        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return post_error("Database connection exception", "An error occurred while connecting to the database:{}".format(str(e)), None)

   