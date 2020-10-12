import config
import json
from models import UserManagementModel

class UserManagementRepositories:
    @staticmethod
    def create_users(users):
        # name,userName,password,email,phoneNo,roleCode,roleDesc
        users = UserManagementModel.create_users(users)
        if users == None:
            return False
        return users
        
    @staticmethod
    def update_users(users):
        # name,userName,password,email,phoneNo,roleCode,roleDesc
        for user in users:
            if UserManagementModel.update_users_by_u_id(users) == False:
                return False
        return True

    @staticmethod
    def search_users(userIDs,userNames,roleCodes):
        result = UserManagementModel.get_user_by_keys(userIDs,userNames,roleCodes)
        return result