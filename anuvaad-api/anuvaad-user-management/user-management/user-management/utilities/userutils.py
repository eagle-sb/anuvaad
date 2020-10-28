import uuid
import re
import bcrypt
from db import get_db
from anuvaad_auditor.loghandler import log_info, log_exception
from anuvaad_auditor.errorhandler import post_error
import jwt
from utilities import MODULE_CONTEXT
import config
import json
import codecs
from app import ROLE_CODES



# role_codes_json= json.load(codecs.open(role_codes_filepath, 'r', 'utf-8-sig'))
# role_codes_data=role_codes_json["roles"]

# print(role_codes_data)

class UserUtils:

    def __init__(self):
        pass

    @staticmethod
    def generate_user_id():
        return(uuid.uuid4().hex)

    @staticmethod
    def validate_email(email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if (re.search(regex, email)):
            return True
        else:
            return False

    @staticmethod
    def validate_phone(phone):
        Pattern = re.compile("(0/91)?[6-9][0-9]{9}")
        if (Pattern.match(phone)) and len(phone) == 10:
            return True
        else:
            return False

    @staticmethod
    def validate_password(password):
        if len(password)<config.MIN_LENGTH:
            return False
        else:
            return True


    @staticmethod
    def hash_password(password):
        password_in_byte = bytes(password, 'utf-8')  # converting str to byte
        salt = bcrypt.gensalt()
        return(bcrypt.hashpw(password_in_byte, salt))

    @staticmethod
    def encrypt_password(password):
        encrypted_password = sha256_crypt.encrypt(password)
        return(encrypted_password)

    @staticmethod
    def validate_userid(usrId):
        collections = get_db()[config.USR_MONGO_COLLECTION]
        valid = collections.find({'userID': {'$in': [usrId]}})
        if valid.count() != 0:
            userID = UserUtils.generate_user_id()
            validate_userid(userID)
        else:
            return(usrId)

    @staticmethod
    def validate_username(usrName):
        collections = get_db()[config.USR_MONGO_COLLECTION]
        valid = collections.find({'userName': {'$in': [usrName]}})
        log_info("search result on db for username validation:{}".format(valid),MODULE_CONTEXT)
        if valid.count() != 0:
            return(False)
        else:
            return(True)

    @staticmethod
    def validate_rolecodes(roles):
        roles=[x.upper() for x in roles]
        for role in roles:
            if role not in ROLE_CODES:
                return False

    @staticmethod
    def validate_user(usrName, password):
        try:
            collections = get_db()[config.USR_MONGO_COLLECTION]
            result = collections.find({'userName': {'$eq': usrName}}, {
                'password': 1, '_id': 0})
            log_info("searching for password of the requested user:{}".format(result),MODULE_CONTEXT)
            if result.count()==0:
                return False
            for value in result:
                password_in_db = value["password"].encode("utf-8")
                log_info("password stored on db is retrieved",MODULE_CONTEXT)
                if bcrypt.checkpw(password.encode("utf-8"), password_in_db):
                    return True
                else:
                    return False
        except Exception as e:
            log_exception("exception while validating username and password"+str(e),  MODULE_CONTEXT, e)
            return None

    @staticmethod
    def token_validation(token):

        token_received=token
        if not token_received:
            return post_error("Invalid token","Token recieved is empty",None)
        else:
            try:
                collections = get_db()[config.USR_TOKEN_MONGO_COLLECTION]
                # print(collections)
                result = collections.find({"token": token_received}, {"_id": 0, "user": 1, "active": 1, "secret_key": 1})
                log_info("searching for record with the recieved token:{}".format(result),MODULE_CONTEXT)
                if result.count() == 0:
                    return post_error("Invalid token","Token recieved is not matching",None)
                for value in result:
                    if value["active"] == False:
                        return post_error("Invalid token","Token has expired", None)         
                    if value["active"] == True:
                        secret_key = value["secret_key"]
                        # user = value["user"]
        
                        try:
                            jwt.decode(token, secret_key, algorithm='HS256')
                            # return ({"status": True, "data": user})
                        except jwt.exceptions.ExpiredSignatureError as e:
                            log_exception("token expired",  MODULE_CONTEXT, e)
                            collections.update({"token": token}, {
                                        "$set": {"active": False}})
                            return post_error("Invalid token","Token has expired", None)
                        except Exception as e:
                            log_exception("invalid token",  MODULE_CONTEXT, e)
                            return post_error("Invalid token", "Not a valid token", None)
            except Exception as e:
                
                log_exception("db connection exception ",  MODULE_CONTEXT, e)                
                return post_error("Database connection exception","An error occurred while connecting to the database",None)

    @staticmethod
    def get_user_from_token(token):
        token_received=token
        try:
            collections = get_db()[config.USR_TOKEN_MONGO_COLLECTION]
            result = collections.find({"token": token_received}, {"_id": 0, "user": 1})
            log_info("search result for username in usertokens db matching the recieved token:{}".format(result),MODULE_CONTEXT)
            for record in result:
                username=record["user"]
                
        except Exception as e:

            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return post_error("Database connection exception","An error occurred while connecting to the database",None)
        try:
            # print(username)
            collections_usr=get_db()[config.USR_MONGO_COLLECTION]
            result_usr = collections_usr.find({"userName": username}, {"_id": 0, "password": 0})
            log_info("record in users db matching the recieved token:{}".format(result),MODULE_CONTEXT)
            for record in result_usr:
                return record
        except Exception as e:

            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return post_error("Database connection exception","An error occurred while connecting to the database",None)


    @staticmethod
    def get_token(userName):
        try:
            collections = get_db()[config.USR_TOKEN_MONGO_COLLECTION]
            record = collections.find(
                {"user": userName, "active": True}, {"_id": 0, "token": 1, "secret_key": 1})
            log_info("search result for an active token matching the username:{}".format(record),MODULE_CONTEXT)
        
            if record.count() == 0:
                return {"status": "No token vailable for the user", "data": None}
            else:
                for value in record:

                    secret_key = value["secret_key"]
                    token = value["token"]
                    try:
                        result = jwt.decode(token, secret_key, algorithm='HS256')
                        return({"status": True, "data": token})
                    except jwt.exceptions.ExpiredSignatureError as e:
                        log_exception("token matching the username has expired "+str(e),  MODULE_CONTEXT, e)
                        collections.update({"token": token}, {
                                        "$set": {"active": False}})
                        return({"status": "Token has expired", "data": None})
                    except Exception as e:
                        log_exception("invalid token for the given username",  MODULE_CONTEXT, e)
                        return({"status": "Invalid token ", "data": None})
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return({"status":"Database connection exception","data":None})

    @staticmethod
    def validate_user_input_creation(user):
        # print(user)
        username = user["userName"]
        password = user["password"]
        email = user["email"]
        phone = user["phoneNo"]
        roles =user["roles"]
        rolecodes=[]

        if not username or not password or not email or not phone or not roles:
            return post_error("Data missing", "Username,password,email,phone numbers,roles are mandatory fields, they cannot be empty", None) 
        if UserUtils.validate_password(password) == False:
            return post_error("Data not valid", "Password given is not valid", None)  
        if UserUtils.validate_email(email) == False:
            return post_error("Data not valid", "Email Id given is not valid", None)
        if UserUtils.validate_phone(phone) == False:
            return post_error("Data not valid", "Phone number given is not valid", None)
        try:
            collections = get_db()[config.USR_MONGO_COLLECTION]
            record = collections.find({'userName':username})
            if record.count() != 0:
                return post_error("Data not valid", "Username given is already taken,try with another username", None)
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return post_error("Database connection exception","An error occurred while connecting to the database",None)
        for rol in roles:
            rolecodes.append(rol["roleCode"])
        if not rolecodes:
            return post_error("Data Missing","No rolecodes are given",None)
        if UserUtils.validate_rolecodes(rolecodes)==False:
            return post_error("Data not valid","Rolecode given is not valid",None)




    @staticmethod
    def validate_user_input_updation(user):
        userId = user["userID"]
        username = user["userName"]
        password = user["password"]
        email = user["email"]
        phone = user["phoneNo"]
        roles =user["roles"]
        rolecodes=[]

        

        if not userId:
            return post_error("Id missing", "UserID field cannot be empty", None)
        if not username or not password or not email or not phone or not roles:
            return post_error("Data missing", "Username,password,email,phone numbers,roles are mandatory fields, they cannot be empty", None)
        if UserUtils.validate_password(password) == False:
            return post_error("Data not valid", "Password given is not valid", None) 
        if UserUtils.validate_email(email) == False:
            return post_error("Data not valid", "Email Id given is not valid", None)
        if UserUtils.validate_phone(phone) == False:
            return post_error("Data not valid", "Phone number given is not valid", None)
        try:
            collections = get_db()[config.USR_MONGO_COLLECTION]
            record = collections.find({'userID':userId})
            if record.count() == 0:
                return post_error("Data not valid", "User Id given is not valid", None)
            for value in record:
                if value["userName"] != username:
                    return post_error("Data not valid","Username is not valid for the given User Id",None)
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return post_error("Database connection exception","An error occurred while connecting to the database",None)
        for rol in roles:
            rolecodes.append(rol["roleCode"])
        if not rolecodes:
            return post_error("Data Missing","No rolecodes are given",None)
        if UserUtils.validate_rolecodes(rolecodes)==False:
            return post_error("Data not valid","Rolecode given is not valid",None)


        
    @staticmethod
    def validate_user_login_input(userName,Password):
        username = userName
        password = Password
        if not username:
            return post_error("Username missing", "Username field cannot be empty", None)
        if not password:
            return post_error("Password missing", "Password field cannot be empty", None)
        if UserUtils.validate_user(username,password)==False:
            return post_error("Invalid credentials","username and password doesn't match",None)
        if UserUtils.validate_user(username,password)==None:
            return post_error("Database connection exception","An error occurred while connecting to the database",None)

    # @staticmethod


        
 
