from utilities import MODULE_CONTEXT
from db import get_db
from utilities import UserUtils
from anuvaad_auditor.loghandler import log_info, log_exception
import bcrypt


class UserManagementModel(object):

    @staticmethod
    def create_users(user):
        hashed = UserUtils.hash_password(user["password"].encode('utf-8'))
        encripted = UserUtils.encrypt_password(hashed)
        userId = UserUtils.generate_user_id()
        validated_userID = UserUtils.validate_userid(userId)
        userName = user['userName']
        validated_userName = UserUtils.validate_username(userName)
        print(validated_userName)
        # try:
        #     if validated_userName == False:
        #         return("UserName is already taken ")

        user_roles = []
        for role in user["roles"]:
            role_info = {}
            role_info["roleCode"] = role["roleCode"]
            role_info["roleDesc"] = role["roleDesc"]
            user_roles.append(role_info)

        try:
            collections = get_db()['sample']
            if validated_userName != False:
                user = collections.insert({'userID': validated_userID, 'name': user["name"], 'userName': validated_userName, 'password': encripted,
                                       'email': user["email"], 'phoneNo': user["phoneNo"], 'roles': user_roles})
                return user
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None

    @staticmethod
    def update_users_by_uid(user):
        try:
            collections = get_db()['sample']
            user_id = user["userID"]

            record = collections.find({"userID": user_id})

            if record == None:
                return("No record for the given user Id")
            else:

                user_roles = []
                for role in user["roles"]:
                    role_info = {}
                    role_info["roleCode"] = role["roleCode"]
                    role_info["roleDesc"] = role["roleDesc"]
                    user_roles.append(role_info)

                hashed = UserUtils.hash_password(
                    user["password"].encode('utf-8'))
                encripted = UserUtils.encrypt_password(hashed)

                results = collections.update({"userID": user_id}, {'$set': {'name': user["name"], 'userName': user['userName'], 'password': hashed,
                                                                            'email': user["email"], 'phoneNo': user["phoneNo"], 'roles': user_roles}})

                if 'writeError' in list(results.keys()):
                    return False
                return True

        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None

    @staticmethod
    def get_user_by_keys(userIDs, userNames, roleCodes):

        exclude = {"_id": False, "password": False}

        try:
            collections = get_db()['sample']
            # out =   db.sample.find({$or:[{'userID': {'$in': ['a7de4c4f7a30491e833cd1fc5b38ba3a']}}, {'userName': {'$in': ['Bjc@123']}},{ 'roles.roleCode': {'$in': ['01']}}]})
            out = collections.find(
                {'$or': [
                    {'userID': {'$in': userIDs}},
                    {'userName': {'$in': userNames}},
                    {'roles.roleCode': {'$in': roleCodes}}
                ]}, exclude)
            # print(out.count())
            result = []
            for record in out:
                result.append(record)

            # print(result)
            return result

        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None
