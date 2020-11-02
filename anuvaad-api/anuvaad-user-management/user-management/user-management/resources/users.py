from flask_restful import fields, marshal_with, reqparse, Resource
from repositories import UserManagementRepositories
from models import CustomResponse, Status
from utilities import UserUtils,MODULE_CONTEXT
import ast
from anuvaad_auditor.loghandler import log_info, log_exception
from flask import request
from flask import jsonify
from anuvaad_auditor.errorhandler import post_error


class CreateUsers(Resource):

    def post(self):
        body = request.get_json()
        print(body.keys())
        if 'users' not in body.keys():
            return post_error("Key error","users not found",None)

        if 'users' in body:
            users = body['users']
        log_info("data recieved for user creation is:{}".format(users),MODULE_CONTEXT)
        if not users:
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400

        for user in users:
            validity = UserUtils.validate_user_input_creation(user)
            log_info("User is validated:{}".format(validity),MODULE_CONTEXT)
            if validity is not None:
                return validity, 400

        if not users:
            res = CustomResponse(
                Status.FAILURE_USR_CREATION.value, None)
            return res.getresjson(), 400
        try:
            result = UserManagementRepositories.create_users(users)
            log_info("User creation result:{}".format(result),MODULE_CONTEXT)
            if result == False:
                res = CustomResponse(
                    Status.FAILURE_USR_CREATION.value, None)
                return res.getresjson(), 400

            res = CustomResponse(Status.SUCCESS_USR_CREATION.value, None)
            return res.getresjson(), 200
        except Exception as e:
            log_exception("Exception while creating user records: " +
                      str(e), MODULE_CONTEXT, e)
            res = CustomResponse(
                Status.FAILURE_USR_CREATION.value, None)
            return res.getresjson(), 400


class UpdateUsers(Resource):

    def post(self):
        body = request.get_json()
        if 'users' not in body.keys():
            return post_error("Key error", "users not found",None)

        users = body['users']
        log_info("data recieved for user updation is:{}".format(users),MODULE_CONTEXT)
        if not users:
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400

        for user in users:
            validity = UserUtils.validate_user_input_updation(user)
            log_info("User is validated: {}".format(validity),MODULE_CONTEXT)
            if validity is not None:
                return validity, 400

        if not users:
            res = CustomResponse(
                Status.FAILURE_USR_UPDATION.value, None)
            return res.getresjson(), 400

        try:
            result = UserManagementRepositories.update_users(users)
            log_info("User updation result:{}".format(result),MODULE_CONTEXT)
            if result == False:
                res = CustomResponse(
                    Status.FAILURE_USR_UPDATION.value, None)
                return res.getresjson(), 400

            res = CustomResponse(Status.SUCCESS.value, None)
            return res.getres()
        except Exception as e:
            log_exception("Exception while updating user records: " +
                      str(e), MODULE_CONTEXT, e)
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400


class SearchUsers(Resource):

    def post(self):

        body = request.get_json()
        if "userIDs" not in body.keys():
            return post_error("Key error","userIDs not found",None)
        if "userNames" not in body.keys():
            return post_error("Key error","userNames not found",None)
        if "roleCodes" not in body.keys():
            return post_error("Key error","roleCodes not found",None)
        

        userIDs = body['userIDs']
        userNames = body['userNames']
        roleCodes = body['roleCodes']
        log_info("data recieved for user search is;user Ids:{}"+'\n'+'user names:{}'+'\n'+"role codes:{}".format(userIDs,userNames,roleCodes),MODULE_CONTEXT)
        if not userIDs and not userNames and not roleCodes:
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400

        try:
            result = UserManagementRepositories.search_users(
                userIDs, userNames, roleCodes)
            log_info("User search result:{}".format(result),MODULE_CONTEXT)
            if result == False:
                res = CustomResponse(
                    Status.FAILURE_USR_SEARCH.value, None)
                return res.getresjson(), 400

            res = CustomResponse(Status.SUCCESS_USR_SEARCH.value, result)
            return res.getresjson(), 200
        except Exception as e:
            log_exception("Exception while searching user records: " +
                      str(e), MODULE_CONTEXT, e)
            res = CustomResponse(
                Status.FAILURE_GLOBAL_SYSTEM.value, None)
            return res.getresjson(), 500

class Health(Resource):
    def get(self):
        response = {"code": "200", "status": "ACTIVE"}
        return jsonify(response)
