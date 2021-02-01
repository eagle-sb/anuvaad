from utilities import MODULE_CONTEXT
from db import get_db
from utilities import UserUtils, OrgUtils
from anuvaad_auditor.loghandler import log_info, log_exception
from anuvaad_auditor.errorhandler import post_error
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
                timeLimit = datetime.datetime.utcnow(
                ) + datetime.timedelta(hours=24)  # set limit for user
                payload = {"userName": userName, "password": str(
                    UserUtils.hash_password(password)), "exp": timeLimit}
                token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') #generating auth token using pyjwt
                collections.insert({"user": userName, "token": token.decode("utf-8"), "secret_key": SECRET_KEY,
                                    "active": True, "start_time": eval(str(time.time()).replace('.', '')[0:13]), "end_time": 0})
                log_info("user login details are stored on db:", MODULE_CONTEXT)
                return_data = {
                    "userName": userName,
                    "token": token.decode("UTF-8")}
                return return_data
            else:
                token_available = UserUtils.get_token(userName)
                log_info("pre generated token for the logged in user:{}".format(
                    token_available), MODULE_CONTEXT)
                token = token_available["data"]
                return_data = {
                    "userName": userName,
                    "token": token}
                return return_data
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return post_error("Database  exception", "An error occurred while processing on the database:{}".format(str(e)), None)

    @staticmethod
    def user_logout(userName):

        try:
            collections = get_db()[config.USR_TOKEN_MONGO_COLLECTION]
            record = collections.find({"user": userName, "active": True})
            log_info("search on db for user logout :{}".format(
                record), MODULE_CONTEXT)
            if record.count() == 0:
                return False

            if record.count() != 0:
                for user in record:
                    results = collections.update(user, {"$set": {"active": False, "end_time": eval(
                        str(time.time()).replace('.', '')[0:13])}})
                    log_info(
                        "re-setting db values on user log out:{}".format(results), MODULE_CONTEXT)
                return True
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return post_error("Database connection exception", "An error occurred while connecting to the database:{}".format(str(e)), None)

    @staticmethod
    def token_search(token,temp):
        try:
            result = UserUtils.get_user_from_token(token,temp)
            log_info("searching for the user, using token", MODULE_CONTEXT)
            return result

        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return post_error("Database connection exception", "An error occurred while connecting to the database:{}".format(str(e)), None)

    @staticmethod
    def forgot_password(userName):

        rand_id=UserUtils.generate_user_id()
        collections = get_db()[config.USR_TEMP_TOKEN_MONGO_COLLECTION]
        collections.insert({"user": userName, "token": rand_id, "start_time": datetime.datetime.utcnow()})
        result = UserUtils.generate_email_reset_password(userName,rand_id)
        if result is not None:
            return result
        return True
    
    @staticmethod
    def reset_password(userId,userName,password):

        hashed = UserUtils.hash_password(password).decode("utf-8")
        try:
            collections = get_db()[config.USR_MONGO_COLLECTION]
            record = collections.find({"userID": userId})
            log_info("search on db for authentication of the userId passed:{}".format(
                record), MODULE_CONTEXT)
            
            if record.count() != 0:
                for user in record:
                    roles=[ rol['roleCode'] for rol in user["roles"] ] 
                    log_info("role of the user matching the userId passed is:{}".format(str(roles)), MODULE_CONTEXT)
                    role_keys=[x.upper() for x in roles]
                    username=user["userName"]
            if ("ADMIN" in role_keys) or (username == userName):
                    log_info("reset rquest is checked against role permission and username", MODULE_CONTEXT)
                    reset_record = collections.find({"userName": userName})
                    log_info("search on db for user record to reset the password:{}".format(
                    record), MODULE_CONTEXT)

                    for user in reset_record:
                        results = collections.update(user, {"$set": {"password": hashed}})
                        if 'writeError' in list(results.keys()):
                            return post_error("db error", "writeError whie updating record", None)
                    return True
            else:
                return post_error("Data Not valid","Invalid Credential",None)
                
        except Exception as e:
            log_exception("db  exception ",  MODULE_CONTEXT, e)
            return post_error("Database exception", "Exception:{}".format(str(e)), None)
           

    @staticmethod
    def verify_user(user_email,user_id):
        try:
            collections = get_db()[config.USR_MONGO_COLLECTION]
            primary_record= collections.find({"userName": user_email,"is_verified": True})
            if primary_record.count()!=0:
                return post_error("Not allowed","This user already have a verified account",None)
         
            record = collections.find({"userName": user_email,"userID":user_id})
            log_info("search on db for user activation :{},record count:{}".format(
                record,record.count()), MODULE_CONTEXT)         
            
            if record.count()==0:
                return post_error("Data Not valid","No records matching the given parameters ",None)
            if record.count() ==1:
                for user in record:
                    results = collections.update(user, {"$set": {"is_verified": True,"is_active":True,"activated_time":eval(str(time.time()))}})
                    if 'writeError' in list(results.keys()):
                            return post_error("db error", "writeError whie updating record", None)
                    log_info(
                        "Activating user account:{}".format(results), MODULE_CONTEXT)
            else:
                return post_error("Data Not valid","Somehow there exist more than one record matching the given parameters ",None)
                
        except Exception as e:
            log_exception("db  exception ",  MODULE_CONTEXT, e)
            return post_error("Database exception", "Exception:{}".format(str(e)), None)

    @staticmethod
    def activate_deactivate_user(user_email,status):
        try:
            collections = get_db()[config.USR_MONGO_COLLECTION]
            record = collections.find({"userName": user_email,"is_verified":True})
            log_info("search on db for user activation/deactivation :{},record count:{}".format(
                record,record.count()), MODULE_CONTEXT)
            if record.count()==0:
                return post_error("Data Not valid","Not a verified user",None)
            if record.count() ==1:
                for user in record:
                    validity=OrgUtils.validate_org(user["orgID"])
                    if validity is not None:
                        return validity
                    results = collections.update(user, {"$set": {"is_active": status}})
                    if 'writeError' in list(results.keys()):
                        return post_error("db error", "writeError whie updating record", None)
                    log_info(
                        "Activating/Deactivating user account:{}".format(results), MODULE_CONTEXT)
            else:
                return post_error("Data Not valid","Somehow there exist more than one record matching the given parameters ",None)
                
        except Exception as e:
            log_exception("db  exception ",  MODULE_CONTEXT, e)
            return post_error("Database exception", "Exception:{}".format(str(e)), None)
           
           
