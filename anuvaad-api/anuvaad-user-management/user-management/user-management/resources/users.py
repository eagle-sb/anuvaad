from flask_restful import fields, marshal_with, reqparse, Resource
from repositories import UserManagementRepositories
from models import CustomResponse, Status
from utilities import UserUtils
import ast
from anuvaad_auditor.loghandler import log_info, log_exception
from flask import request
from flask import jsonify
from anuvaad_auditor.errorhandler import post_error


class CreateUsers(Resource):

    def post(self):

        # print(UserUtils.read_role_codes())

        body = request.get_json()
        if 'users' in body:
            users = body['users']
        if not users:
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400

        for user in users:
            validity = UserUtils.validate_user_input_creation(user)
            if validity is not None:
                return validity, 400

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
            return res.getresjson(), 200
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
            validity = UserUtils.validate_user_input_updation(user)
            # print(validity,"here")
            if validity is not None:
                return validity, 400

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
        userIDs = body['userIDs']
        userNames = body['userNames']
        roleCodes = body['roleCodes']

        if not userIDs and not userNames and not roleCodes:
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400

        try:
            result = UserManagementRepositories.search_users(
                userIDs, userNames, roleCodes)
            # print(result)
            if result == False:
                res = CustomResponse(
                    Status.FAILURE_USR_SEARCH.value, None)
                return res.getresjson(), 400

            res = CustomResponse(Status.SUCCESS_USR_SEARCH.value, result)
            return res.getresjson(), 200
        except Exception as e:
            res = CustomResponse(
                Status.FAILURE_GLOBAL_SYSTEM.value, None)
            return res.getresjson(), 500

class Health(Resource):
    def get(self):
        response = {"code": "200", "status": "ACTIVE"}
        return jsonify(response)
