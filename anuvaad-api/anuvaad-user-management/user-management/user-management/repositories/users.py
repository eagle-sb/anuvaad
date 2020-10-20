import config
import json
from models import UserManagementModel


class UserManagementRepositories:

    @staticmethod
    def create_users(users):
        if UserManagementModel.create_users(users)!=True:
            return False

    @staticmethod
    def update_users(users):
        if UserManagementModel.update_users_by_uid(users)!= True:
            return False

    @staticmethod
    def search_users(userIDs, userNames, roleCodes):
        result = UserManagementModel.get_user_by_keys(
            userIDs, userNames, roleCodes)
        # print(result)
        return result
