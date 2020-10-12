from utilities import MODULE_CONTEXT
from db import get_db
from utilities import hash_password, encrypt_password, generate_user_id 
from anuvaad_auditor.loghandler import log_info, log_exception
import bcrypt

class UserManagementModel(object):

    @staticmethod
    def create_users(name,userName,password,email,phoneNo,roleCode,roleDesc):
        hashed        = hash_password(password.encode('utf-8'))
        # encripted     = encrypt_password(hashed)
        userID        = generate_user_id()
    
        try:
            collections = get_db()['sample']
            user         = collections.insert({'userID': userID,'name':name,'userName': userName,'password':hashed,
                                                   'email': email,'phoneNo': phoneNo,'roles':[{'roleCode':roleCode,'roleDesc':roleDesc}]})
            return user
        except Exception as e:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None
        
    @staticmethod
    def update_users_by_u_id(user_id, s_id):
        try:
            collections = get_db()['sample']
            record=collections.find({"userID": user_id})
            response = record.update_one({'$set': {'name':name,'userName': userName,'password':encripted,
                                                   'email': email,'phoneNo': phoneNo,'roles':[{'roleCode':roleCode,'roleDesc':roleDesc}]}})

            output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
            return output
        except expression as identifier:
            log_exception("db connection exception ",  MODULE_CONTEXT, e)
            return None

    # @staticmethod
    # def get_user_by_keys(user_id, sentence):
    #     SENTENCE_KEYS   = ['n_id', 'pred_score', 's_id', 'src', 'tgt']
    #     try:
    #         collections     = get_db()['file_content']

            # results         = collections.update({'$and': [{'created_by': user_id}, { 'data.tokenized_sentences': {'$elemMatch': {'s_id': {'$eq': sentence['s_id']}}}}]},
            #                                     {
            #                                         '$set':
            #                                         {
            #                                             "data.tokenized_sentences.$.n_id" : sentence['n_id'],
            #                                             "data.tokenized_sentences.$.src"  : sentence['src'],
            #                                             "data.tokenized_sentences.$.tgt"  : sentence['tgt'],
            #                                         }
            #                                     }, upsert=False)

    #         if 'writeError' in list(results.keys()):
    #             return False
    #         return True        
    #     except expression as identifier:
    #         log_exception("db connection exception ",  MODULE_CONTEXT, e)
    #         return False
