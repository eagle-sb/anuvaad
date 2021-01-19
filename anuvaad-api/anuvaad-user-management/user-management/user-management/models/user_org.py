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
        records = []
        for org in orgs:
            org_data = {}
            orgId =OrgUtils.generate_org_id()

            org_data['orgID'] = orgId
            org_data['code'] =str(org["code"]).upper()
            org_data['active'] = org["active"]
            org_data['description'] = org["description"]
            
            records.append(org_data)
        log_info("Org records:{}".format(records), MODULE_CONTEXT)

        if not records:
            return post_error("Data Null", "data recieved for insert operation is null", None)
        try:
            collections = get_db()[config.USR_ORG_MONGO_COLLECTION]
            results = collections.insert(records)
            if len(records) != len(results):
                return post_error("db error", "some of the records were not inserted into db", None)
            log_info("organizations created:{}".format(results), MODULE_CONTEXT)
            

        except Exception as e:
            log_exception("db connection exception " +
                          str(e),  MODULE_CONTEXT, e)
            return post_error("Database  exception", "An error occurred while processing on the db :{}".format(str(e)), None)

    @staticmethod
    def update_orgs_by_orgid(orgs):
        try:
            for org in orgs:
                collections = get_db()[config.USR_ORG_MONGO_COLLECTION]
                org_id = org["orgID"]
                
                org_data = {}
                org_data['code'] = str(org["code"]).upper()
                org_data['active'] = org["active"]
                org_data['description'] = org["description"]
                results = collections.update(
                    {"orgID": org_id}, {'$set': org_data}, upsert=True)
                if 'writeError' in list(results.keys()):
                    return post_error("db error", "some of the records where not updated", None)
                log_info("org updated:{}".format(results), MODULE_CONTEXT)

        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return post_error("Database connection exception", "An error occurred while connecting to the database:{}".format(str(e)), None)

    @staticmethod
    def get_orgs_by_keys(org_code):
        

        exclude = {"_id":False}

        try:
            collections = get_db()[config.USR_ORG_MONGO_COLLECTION]
            if org_code== None :
                out = collections.find({},exclude)
                record_count=out.count()
            else:
                out = collections.find({"code":org_code}, exclude)
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

   