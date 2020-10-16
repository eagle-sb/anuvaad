import uuid
import re
import bcrypt
from db import get_db
from passlib.hash import sha256_crypt

class UserUtils:

    def __init__(self):
        pass

    def generate_user_id():
        return(uuid.uuid4().hex)

    def validate_email(email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if (re.search(regex, email)):
            return email
        else:
            return("Invalid mail id")

    def validate_phone(phone):
        Pattern = re.compile("(0/91)?[6-9][0-9]{9}")
        if (Pattern.match(phone)) and len(phone) == 10:
            return phone
        else:
            return("Invalid phone number")

    def hash_password(password):
        salt = bcrypt.gensalt()
        return(bcrypt.hashpw(password, salt))


    def encrypt_password(password):
            encrypted_password = sha256_crypt.encrypt(password)
            return(encrypted_password)



    def validate_userid(usrId):
            collections = get_db()['sample']
            valid = collections.find({ 'userID': {'$in': [usrId]}})
            if valid.count() != 0:
                    userID = UserUtils.generate_user_id()
                    validate_userid(userID)
            else:
                    return(usrId)

    def validate_username(usrName):
            collections = get_db()['sample']
            valid = collections.find({ 'userName': {'$in': [usrName]}})
            if valid.count() != 0:
                    return(False)
            else:
                    return(usrName)

                    
    def validate_user(usrName,password):
        collections = get_db()['sample']
        result= collections.find({'userName': {'$eq':usrName }},{'password':1,'_id':0})
        for value in result:
            password_in_db=value["password"]
        print(password_in_db)
        # print(password)
        if sha256_crypt.verify(password_in_db, password) == True:
            return True
        else:
            return False



