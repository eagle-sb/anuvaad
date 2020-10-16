import config
import json
from models import UserAuthenticationModel


class UserAuthenticationRepositories:

    @staticmethod
    def user_login(userName,password):
        
        if UserAuthenticationModel.user_login(userName,password) == False:
                return False

        return True