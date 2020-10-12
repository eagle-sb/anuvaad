from flask_restful import fields, marshal_with, reqparse, Resource
from repositories import UserManagementRepositories
from models import CustomResponse, Status
# from utilities import AppContext
import ast
from anuvaad_auditor.loghandler import log_info, log_exception
from flask import request
class CreateUsers(Resource):
    
    def post(self):
        
        body        = request.get_json()
        users       = None
        if 'users' in body:
            users   = body['users']

        if users is None:
            response = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return response.getresjson(), 400

        # AppContext.addRecordID(None)
        # log_info("SaveSentenceResource for user {}, number sentences to update {}".format(user_id, len(sentences)), AppContext.getContext())


        try:
            result = UserManagementRepositories.create_users(users)
            if result == False:
                res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
                return res.getresjson(), 400

            res = CustomResponse(Status.SUCCESS.value, result)
            return res.getres()
        except Exception as e:
            # log_exception("SaveSentenceResource ",  AppContext.getContext(), e)
            res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400


class UpdateUsers(Resource):

    def post(self):
        body        = request.get_json()
        userID     = request.headers.get('userID')
        
        if 'users' not in body or user_id is None:
            res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400
        
        users      = body['users']
        # AppContext.addRecordID(None)
        # log_info("FileContentUpdateResource for user ({}), to update ({}) blocks".format(user_id, len(blocks)), AppContext.getContext())

        try:
            result  = UserManagementRepositories.update_users(userID, users)

            if result == False:
                res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
                return res.getresjson(), 400

            # log_info("FileContentUpdateResource for user ({}) updated".format(user_id), AppContext.getContext())
            res = CustomResponse(Status.SUCCESS.value, result, None)
            return res.getres()            
        except Exception as e:
            # log_exception("FileContentGetResource ",  AppContext.getContext(), e)
            res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400
        

# class SearchUser(Resource):

#     def post(self):
#         parser = reqparse.RequestParser(bundle_errors=True)

#         parser.add_argument('userIDs', type=list, location='json', help='This field cannot be empty', required=True)
#         parser.add_argument('userNames', type=list, location='json', help='This field cannot be empty', required=True)
#         parser.add_argument('roleCodes',  type=list, location='json', help='This field cannot be empty', required=True)

#         args    = parser.parse_args()

#         if UserManagementRepositories.search(args['userIDs'], args['userNames'], args['roleCodes']) == False:
#             res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
#             return res.getresjson(), 400
#         res = CustomResponse(Status.SUCCESS.value, None)
#         return res.getres()




  

        # parser = reqparse.RequestParser(bundle_errors=True)

        # parser.add_argument('userID', type=str, location='json', help='UserId cannot be empty', required=True)
        # parser.add_argument('name', type=str, location='json', help='Name cannot be empty', required=True)
        # parser.add_argument('userName',  type=str, location='json', help='UserName cannot be empty', required=True)
        # parser.add_argument('password', type=str, location='json',help='Password cannot be empty', required=True)
        # parser.add_argument('email', type=str, location='json', help='Email is required', required=False)
        # parser.add_argument('phoneNo', type=str, location='json', help='Phone number is required', required=True)
        # parser.add_argument('roleCode', type=str, location='json', help='Role code are required', required=True)
        # parser.add_argument('roleDesc', type=str, location='json', help='Role description required', required=True)
        # args    = parser.parse_args()
