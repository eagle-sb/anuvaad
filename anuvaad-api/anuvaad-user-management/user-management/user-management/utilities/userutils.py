import uuid
import re
import bcrypt
from db import get_db
from anuvaad_auditor.loghandler import log_info, log_exception
import jwt
from utilities import MODULE_CONTEXT


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
        collections = get_db()['sample']
        valid = collections.find({'userID': {'$in': [usrId]}})
        if valid.count() != 0:
            userID = UserUtils.generate_user_id()
            validate_userid(userID)
        else:
            return(usrId)

    @staticmethod
    def validate_username(usrName):
        collections = get_db()['sample']
        valid = collections.find({'userName': {'$in': [usrName]}})
        # print(valid.count(),"count")
        if valid.count() != 0:
            return(False)
        else:
            return(True)

    @staticmethod
    def validate_user(usrName, password):
        try:
            collections = get_db()['sample']
            result = collections.find({'userName': {'$eq': usrName}}, {
                'password': 1, '_id': 0})
            for value in result:
                password_in_db = value["password"].encode("utf-8")
                if bcrypt.checkpw(password.encode("utf-8"), password_in_db):
                    # print("check",bcrypt.checkpw(password.encode("utf-8"),password_in_db))
                    return True
                else:
                    return False
        except Exception as e:
            log_exception("Invalid credentials ",  MODULE_CONTEXT, e)
            return None

    @staticmethod
    def token_validation(token):

        collections = get_db()['usertokens']
        result = collections.find(
            {"token": token}, {"_id": 0, "user": 1, "active": 1, "secret_key": 1})
        # print(result,"result")
        for value in result:
            # print(value)
            if value["active"] == True:
                secret_key = value["secret_key"]
                user = value["user"]
                try:
                    data = jwt.decode(token, secret_key, algorithm='HS256')
                    # print(data)
                    return({"status": True, "data": user})
                except jwt.exceptions.ExpiredSignatureError:
                    collections.update({"token": token}, {
                                       "$set": {"active": False}})
                    return({"status": "Token has expired", "data": None})
                except:
                    return({"status": "Invalid token", "data": None})

    @staticmethod
    def get_token(userName):
        collections = get_db()['usertokens']
        record = collections.find(
            {"user": userName, "active": True}, {"_id": 0, "token": 1})
        if record.count() == 0:
            return {"status": "No token vailable for the user", "data": None}
        else:
            for value in record:

                secret_key = value["secret_key"]
                token = value["token"]
                try:
                    result = jwt.decode(token, secret_key, algorithm='HS256')
                    return({"status": True, "data": token})
                except jwt.exceptions.ExpiredSignatureError:
                    collections.update({"token": token}, {
                                       "$set": {"active": False}})
                    return({"status": "Token has expired", "data": None})
                except:
                    return({"status": "Invalid token", "data": None})

    @staticmethod
    def validate_user_input(user):
        username = user["userName"]
        password = user["password"]
        email = user["email"]
        phone = user["phoneNo"]
        if not username or not password or not email or not phone:
            return False
        if UserUtils.validate_email(email) == False:
            return False
        if UserUtils.validate_phone(phone) == False:
            return False
