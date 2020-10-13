import uuid
import re
import bcrypt
from cryptography.fernet import Fernet


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
                pass
        
        def hash_password(password):
                salt = bcrypt.gensalt()
                return(bcrypt.hashpw(password, salt))



        def generate_key():
                """
                Generates a key and save it into a file
                """
                key = Fernet.generate_key()
                with open("secret.key", "wb") as key_file:
                        key_file.write(key)

        def load_key():
                """
                Load the previously generated key
                """
                return open("secret.key", "rb").read()

        def encrypt_password(password):
                """
                Encrypts a message
                """
                key = load_key()
                encoded_password = password.encode()
                f = Fernet(key)
                encrypted_password = f.encrypt(encoded_password)
                return(encrypted_password)

                # def decrypt_password(encrypted_password):
                #     """
                #     Decrypts an encrypted message
                #     """
                #     key = load_key()
                #     f = Fernet(key)
                #     decrypted_password = f.decrypt(encrypted_password)
                #     return(decrypted_password.decode())
