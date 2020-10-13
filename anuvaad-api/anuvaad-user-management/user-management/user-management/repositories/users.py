import config
import json
from models import UserManagementModel

class UserManagementRepositories:
    @staticmethod
    def create_users(users):

        for user in users:
            if UserManagementModel.create_users(user)== False:
                return False
            
        return True
        
        # name,userName,password,email,phoneNo,roleCode,roleDesc
        # user_list = []
        
        # for user in users:
        #     user_attributes={}
        #     user_attributes["name"]   = user["name"]
        #     user_attributes["userName"]   = user["userName"]
        #     user_attributes["password"]   = user["password"]
        #     user_attributes["email"]   = user["email"]
        #     user_attributes["phoneNo"]   = user["phoneNo"]

        #     roles= user["roles"]
        #     for role in roles:
        #         roles["roleCode"]
        #         roles["roleDesc"]*

        #     user_attributes["userName"]   = user["userName"]
        #     user_attributes["userName"]   = user["userName"]





    @staticmethod
    def update_users(users):
        # name,userName,password,email,phoneNo,roleCode,roleDesc
        for user in users:
            if UserManagementModel.update_users_by_uid(user) == False:
                return False
        return True

    @staticmethod
    def search_users(userIDs,userNames,roleCodes):
        result = UserManagementModel.get_user_by_keys(userIDs,userNames,roleCodes)
        return result