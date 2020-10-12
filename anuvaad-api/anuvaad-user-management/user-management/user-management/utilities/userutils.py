import uuid
import re


def generate_user_id():
        return(uuid.uuid4().hex)

# class userutils:

#     def __init__(self):
#          pass
    
#     def generate_user_id():
#         return(uuid.uuid4().hex)

#     def validate_email(email):
#         regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
#         if (re.search(regex,email)):
#             return email
#         else:
#             return("Invalid mail id")


    # def validate_phone(phone):
        