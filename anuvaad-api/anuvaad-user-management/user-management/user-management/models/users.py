from utilities import MODULE_CONTEXT
from db import get_db
from utilities import UserUtils
from anuvaad_auditor.loghandler import log_info, log_exception
import bcrypt
from anuvaad_auditor.errorhandler import post_error
import config


class UserManagementModel(object):

    @staticmethod
    def create_users(users):
        records=[]
        for user in users:
            users_data={}
            hashed = UserUtils.hash_password(user["password"])
            log_info("hash created:{}".format(hashed),MODULE_CONTEXT)
            userId = UserUtils.generate_user_id()
            validated_userID = UserUtils.validate_userid(userId)
            log_info("user Id validated:{}".format(validated_userID),MODULE_CONTEXT)
            user_roles = []
            for role in user["roles"]:
                role_info = {}
                role_info["roleCode"] = role["roleCode"].upper()
                role_info["roleDesc"] = role["roleDesc"]
                user_roles.append(role_info)
            log_info("User roles:{}".format(user_roles),MODULE_CONTEXT)

            users_data['userID']=validated_userID
            users_data['name']=user["name"]
            users_data['userName']=user["userName"]
            users_data['password']=hashed.decode("utf-8")
            users_data['email']=user["email"]
            users_data['phoneNo']=user["phoneNo"]
            users_data['roles']=user_roles

            records.append(users_data)
        log_info("User records:{}".format(records),MODULE_CONTEXT)

        if not records:
            return(False)
        try:
            collections = get_db()[config.USR_MONGO_COLLECTION]
            result=collections.insert(records)
            log_info("users created:{}".format(result),MODULE_CONTEXT)
            return True

        # except  result.writeError as e:
        #     log_exception("write error in db"+str(e),MODULE_CONTEXT,e)
        except Exception as e:
            log_exception("db connection exception "+str(e),  MODULE_CONTEXT, e)
            return None

    @staticmethod
    def update_users_by_uid(users):
        try:
            for user in users:
                collections = get_db()[config.USR_MONGO_COLLECTION]
                user_id = user["userID"]
                users_data={}
                userName = user['userName']
                hashed = UserUtils.hash_password(user["password"])
                log_info("hash created:{}".format(hashed),MODULE_CONTEXT)
                    
                user_roles = []
                for role in user["roles"]:
                    role_info = {}
                    role_info["roleCode"] = role["roleCode"].upper()
                    role_info["roleDesc"] = role["roleDesc"]
                    user_roles.append(role_info)

         


                users_data['name']=user["name"]
                users_data['userName']=userName
                users_data['password']=hashed.decode("utf-8")
                users_data['email']=user["email"]
                users_data['phoneNo']=user["phoneNo"]
                users_data['roles']=user_roles

                results=collections.update({"userID": user_id},{'$set':users_data})
                log_info("user updated:"+results,MODULE_CONTEXT)

            return True

        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None

    @staticmethod
    def get_user_by_keys(userIDs, userNames, roleCodes):

        exclude = {"_id": False, "password": False}

        try:
            collections = get_db()[config.USR_MONGO_COLLECTION]
            out = collections.find(
                {'$or': [
                    {'userID': {'$in': userIDs}},
                    {'userName': {'$in': userNames}},
                    {'roles.roleCode': {'$in': roleCodes}}
                ]}, exclude)
            log_info("user search is executed:"+out,MODULE_CONTEXT)
            result = []
            for record in out:
                result.append(record)
            return result

        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None


