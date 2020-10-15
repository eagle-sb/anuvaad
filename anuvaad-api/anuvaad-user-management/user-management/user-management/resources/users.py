from flask_restful import fields, marshal_with, reqparse, Resource
from repositories import UserManagementRepositories
from models import CustomResponse, Status
# from utilities import AppContext
import ast
from anuvaad_auditor.loghandler import log_info, log_exception
from flask import request


class CreateUsers(Resource):

    def post(self):

        body = request.get_json()
        # print(body)
        users = None
        if 'users' in body:
            users = body['users']
        
        # print(users)
        if users is None:
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400

        not_valid=[]
        for user in users:
            if not user["userName"] or user["password"] or user["email"] or user["phoneNo"]:
                res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400





        try:
            result = UserManagementRepositories.create_users(users)
            print(result)
            if result == False:
                res = CustomResponse(
                    Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
                return res.getresjson(), 400

            res = CustomResponse(Status.SUCCESS.value, result)
            return res.getres()
        except Exception as e:
            print(e)
            # log_exception("SaveSentenceResource ",  AppContext.getContext(), e)
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400


class UpdateUsers(Resource):

    def post(self):
        body = request.get_json()
        # userID     = request.headers.get('userID')
        print(body.keys())

        if 'users' not in body.keys():
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400

        users = body['users']
        # print(users)
        # AppContext.addRecordID(None)
        # log_info("FileContentUpdateResource for user ({}), to update ({}) blocks".format(user_id, len(blocks)), AppContext.getContext())

        try:
            result = UserManagementRepositories.update_users(users)
            # print(result)
            if result == False:
                res = CustomResponse(
                    Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
                return res.getresjson(), 400

            res = CustomResponse(Status.SUCCESS.value, result, None)
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
