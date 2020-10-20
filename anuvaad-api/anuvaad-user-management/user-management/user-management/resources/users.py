from flask_restful import fields, marshal_with, reqparse, Resource
from repositories import UserManagementRepositories
from models import CustomResponse, Status
from utilities import UserUtils
import ast
from anuvaad_auditor.loghandler import log_info, log_exception
from flask import request


class CreateUsers(Resource):

    def post(self):
        body = request.get_json()
        if 'users' in body:
            users = body['users']
        if not users:
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400

        for user in users:
            if UserUtils.validate_user_input(user) == False:
                users=users.remove(user)
        # print(users)
        if not users:
            res = CustomResponse(
                        Status.FAILURE_USR_CREATION.value, None)
            return res.getresjson(), 400
        try:
            result = UserManagementRepositories.create_users(users)
            if result == False:
                res = CustomResponse(
                    Status.FAILURE_USR_CREATION.value, None)
                return res.getresjson(), 400

            res = CustomResponse(Status.SUCCESS_USR_CREATION.value, None)
            return res.getresjson() , 200
        except Exception as e:
            # print(e,"exxx")
            res = CustomResponse(
                Status.FAILURE_USR_CREATION.value, None)
            return res.getresjson(), 400


class UpdateUsers(Resource):

    def post(self):
        body = request.get_json()
        users = body['users']

        if not users:
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400

        for user in users:
        
            if UserUtils.validate_user_input(user) == False:
                users=users.remove(user)

        if not users:
            res = CustomResponse(
                        Status.FAILURE_USR_UPDATION.value, None)
            return res.getresjson(), 400
        
        try:
            result = UserManagementRepositories.update_users(users)
    
            if result == False:
                res = CustomResponse(
                        Status.FAILURE_USR_UPDATION.value, None)
                return res.getresjson(), 400

            res = CustomResponse(Status.SUCCESS.value, None)
            return res.getres()
        except Exception as e:
            # print(e)
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400


class SearchUsers(Resource):

    def post(self):

        body = request.get_json()
        if 'userIDs' in body:
            userIDs = body['userIDs']
        else:
            userIDs = None

        if 'userNames' in body:
            userNames = body['userNames']
        else:
            userNames = None

        if 'roleCodes' in body:
            roleCodes = body['roleCodes']
        else:
            roleCodes = None

        try:
            result = UserManagementRepositories.search_users(
                userIDs, userNames, roleCodes)
            # print(result)
            if result == False:
                res = CustomResponse(
                    Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
                return res.getresjson(), 400

            res = CustomResponse(Status.SUCCESS.value, result)
            return res.getres()
        except Exception as e:
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400


#     username = user["userName"]
        #     password = user["password"]
        #     email = user["email"]
        #     phone = user["phoneNo"]
        #     print(user,username,password,email,phone,"00000000")
        #     # print(UserUtils.validate_email(email),"validate",email)
        #     if not username or not password or not email or not phone:
        #         users.remove(user)
        #     else:
        #         valid_users.append(user)
        #     print(valid_users,"validdd")


                # continue
            # if UserUtils.validate_email(email) != True or UserUtils.validate_phone(phone) != True:
            #     users.remove(user)
                # print(users,"users-----------------")
                # continue
                # print(users,"final")
                # if not users:
                #     res = CustomResponse(
                #         Status.FAILURE_USR_UPDATION.value, None)
                #     return res.getresjson(), 400

                
                # if not users:
                #     res = CustomResponse(Status.FAILURE_USR_UPDATION.value, None)
                # return res.getresjson(), 400