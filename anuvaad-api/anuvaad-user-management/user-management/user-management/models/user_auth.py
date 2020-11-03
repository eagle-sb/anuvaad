from utilities import MODULE_CONTEXT
from db import get_db
from utilities import UserUtils
from anuvaad_auditor.loghandler import log_info, log_exception
import bcrypt
import jwt
import datetime
import secrets
from utilities import UserUtils
import time
import config
SECRET_KEY = secrets.token_bytes()


class UserAuthenticationModel(object):

    @staticmethod
    def user_login(userName, password):

        try:
            collections = get_db()[config.USR_TOKEN_MONGO_COLLECTION]
            if (UserUtils.get_token(userName)["status"] != True):
                timeLimit = datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)  # set limit for user
                payload = {"userName": userName, "password": str(
                UserUtils.hash_password(password)), "exp": timeLimit}
                token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
                collections.insert({"user": userName, "token": token.decode("utf-8"), "secret_key": SECRET_KEY, "active": True, "start_time": eval(str(time.time()).replace('.', '')[0:13]), "end_time": 0})
                # if 'writeError' in list(results.keys()):
                #     return False
                log_info("user login details are stored on db:",MODULE_CONTEXT) 
                return_data = {
                    "userName": userName,
                    "token": token.decode("UTF-8")}
                return return_data
            else:
                token_available=UserUtils.get_token(userName)
                log_info("pre generated token for the logged in user:{}".format(token_available),MODULE_CONTEXT)
                token=token_available["data"]
                return_data = {
                    "userName": userName,
                    "token": token}
                return return_data
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None

    @staticmethod
    def user_logout(userName):

        try:
            collections = get_db()[config.USR_TOKEN_MONGO_COLLECTION]
            record = collections.find({"user": userName,"active": True})
            log_info("search on db for user logout :{}".format(record),MODULE_CONTEXT)
            if record.count() == 0:
                return False

            if record.count() != 0:
                for user in record:
                    results = collections.update(user,{"$set":{"active": False, "end_time": eval(
                    str(time.time()).replace('.', '')[0:13])}})
                    log_info("re-setting db values on user log out:{}".format(results),MODULE_CONTEXT)
                return True
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None

    @staticmethod
    def token_search(token):
        try:
            result=UserUtils.get_user_from_token(token)
            log_info("searching for the user, using token",MODULE_CONTEXT)
            return result   

        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None


