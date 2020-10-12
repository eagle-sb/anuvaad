from flask_restful import fields, marshal_with, reqparse, Resource
from repositories import UserManagementRepositories
from models import CustomResponse, Status
import ast
from anuvaad_auditor.loghandler import log_info, log_exception

class CreateUser(Resource):
    
    def post(self):
        
        # log_info("CreateUser log for user {}".format(args['userID']), MODULE_CONTEXT)

        parser = reqparse.RequestParser(bundle_errors=True)

        # parser.add_argument('userID', type=str, location='json', help='UserId cannot be empty', required=True)
        parser.add_argument('name', type=str, location='json', help='Name cannot be empty', required=True)
        parser.add_argument('userName',  type=str, location='json', help='UserName cannot be empty', required=True)
        parser.add_argument('password', type=str, location='json',help='Password cannot be empty', required=True)
        parser.add_argument('email', type=str, location='json', help='Email is required', required=False)
        parser.add_argument('phoneNo', type=str, location='json', help='Phone number is required', required=True)
        parser.add_argument('roleCode', type=str, location='json', help='Role code are required', required=True)
        parser.add_argument('roleDesc', type=str, location='json', help='Role description required', required=True)
        args    = parser.parse_args()

        
        # try:
        #     roles = ast.literal_eval(args['roles'])
        # except expression as identifier:
        #     res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
        #     return res.getresjson(), 400

        if UserManagementRepositories.create_users(args['name'], args['userName'], args['password'], args['email'], args['phoneNo'], args['roleCode'], args['roleDesc']) == False:
            res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400
        res = CustomResponse(Status.SUCCESS.value, None)
        return res.getres()

class UpdateUser(Resource):

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)

        # parser.add_argument('userID', type=str, location='json', help='UserId cannot be empty', required=True)
        parser.add_argument('name', type=str, location='json', help='Name cannot be empty', required=True)
        parser.add_argument('userName',  type=str, location='json', help='UserName cannot be empty', required=True)
        parser.add_argument('password', type=str, location='json',help='Password cannot be empty', required=True)
        parser.add_argument('email', type=str, location='json', help='Email is required', required=False)
        parser.add_argument('phoneNo', type=str, location='json', help='Phone number is required', required=True)
        parser.add_argument('roleCode', type=str, location='json', help='Role code are required', required=True)
        parser.add_argument('roleDesc', type=str, location='json', help='Role description required', required=True)

        args    = parser.parse_args()

        # try:
        #     roles = ast.literal_eval(args['roles'])
        # except expression as identifier:
        #     res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
        #     return res.getresjson(), 400

        if UserManagementRepositories.update_users(args['name'], args['userName'], args['password'], args['email'], args['phoneNo'], args['roleCode'], args['roleDesc']) == False:
            res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400
        res = CustomResponse(Status.SUCCESS.value, None)
        return res.getres()

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