import config
import json
from models import UserManagementModel


class UserManagementRepositories:
    @staticmethod
    def create_users(users):
        for user in users:
            if UserManagementModel.create_users(user) == False:
                return False

        return True

    @staticmethod
    def update_users(users):
        for user in users:
            if UserManagementModel.update_users_by_uid(user) == False:
                return False
        return True

    @staticmethod
    def search_users(userIDs, userNames, roleCodes):
        result = UserManagementModel.get_user_by_keys(
            userIDs, userNames, roleCodes)
        # print(result)
        return result
