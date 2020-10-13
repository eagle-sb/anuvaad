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
        users = None
        if 'users' in body:
            users = body['users']

        if users is None:
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400

        # AppContext.addRecordID(None)
        # log_info("SaveSentenceResource for user {}, number sentences to update {}".format(user_id, len(sentences)), AppContext.getContext())

        try:
            result = UserManagementRepositories.create_users(users)
            if result == False:
                res = CustomResponse(
                    Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
                return res.getresjson(), 400

            res = CustomResponse(Status.SUCCESS.value, result)
            return res.getres()
        except Exception as e:
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
        print(users)
        # AppContext.addRecordID(None)
        # log_info("FileContentUpdateResource for user ({}), to update ({}) blocks".format(user_id, len(blocks)), AppContext.getContext())

        try:
            result = UserManagementRepositories.update_users(users)
            print(result)
            if result == False:
                res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
                return res.getresjson(), 400

            res = CustomResponse(Status.SUCCESS.value, result, None)
            return res.getres()
        except Exception as e:
            print(e)
            res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400


class SearchUsers(Resource):

    def post(self):

        body = request.get_json()
        # users       = None
        if 'userIDs' in body:
            userIDs = body['userIDs']
        else:
            userIDs= None

        if 'userNames' in body:
            userNames = body['userNames']
        else:
            userNames=None

        if 'roleCodes' in body:
            roleCodes = body['roleCodes']
        else:
            roleCodes=None

        # print(userIDs, userNames, roleCodes)

        try:
            result = UserManagementRepositories.search_users(userIDs, userNames, roleCodes)
            # print(result)
            if result == False:
                res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
                return res.getresjson(), 400

            res = CustomResponse(Status.SUCCESS.value, result)
            return res.getres()
        except Exception as e:
            res = CustomResponse(Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400

