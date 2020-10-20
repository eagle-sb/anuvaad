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
SECRET_KEY = secrets.token_bytes()


class UserAuthenticationModel(object):

    @staticmethod
    def user_login(userName, password):

        try:
            collections = get_db()['usertokens']
            if (UserUtils.validate_user(userName, password) == True) and (UserUtils.get_token(userName)["status"] != True):
                timeLimit = datetime.datetime.utcnow(
                ) + datetime.timedelta(seconds=1800)  # set limit for user
                payload = {"userName": userName, "password": str(
                    UserUtils.hash_password(password)), "exp": timeLimit}
                token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

                # print(token,"token")
                collections.insert({"user": userName, "token": token.decode("utf-8"), "secret_key": SECRET_KEY, "active": True, "start_time": eval(
                    str(time.time()).replace('.', '')[0:13]), "end_time": 0})
            else:
                token_available=UserUtils.get_token(userName)
                token=token_available["data"]
                return_data = {
                    "userName": userName,
                    "token": token.decode("UTF-8")
                }
                return return_data
            # else:
            #     return False
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None

    @staticmethod
    def user_logout(userName):

        try:
            collections = get_db()['usertokens']
            record = collections.find({"user": userName})
            print(record.count())
            if record.count() == 0:
                return False

            if record.count() != 0:
                results = collections.update({"user": userName},{"$set":{"active": False, "end_time": eval(
                    str(time.time()).replace('.', '')[0:13])}})
                if 'writeError' in list(results.keys()):
                    return False
                return True
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None

    @staticmethod
    def token_search(token):
        try:
            validated_token=UserUtils.token_validation(token)
            # print(validated_token)
            if validated_token["status"]==True:
                userName=validated_token["data"]
                exclude = {"_id": False, "password": False}
                result = get_db()['sample'].find(
                            {'userName':userName }, exclude)
                for record in result:
                    return record
            if validated_token["status"]!=True:
                return False

        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None


