from utilities import MODULE_CONTEXT
from db import get_db
from utilities import UserUtils
from anuvaad_auditor.loghandler import log_info, log_exception
import bcrypt


class UserAuthenticationModel(object):

    @staticmethod
    def user_login(userName,password):
        
        try:
            collections = get_db()['sample']
            hashed = UserUtils.hash_password(password.encode('utf-8'))
            print(hashed)
            encripted = UserUtils.encrypt_password(hashed)
            if UserUtils.validate_user(userName,encripted) == True:
                return True
            else:
                return False
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None