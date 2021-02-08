from flask_restful import fields, marshal_with, reqparse, Resource
from repositories import UserManagementRepositories
from models import CustomResponse, Status
from utilities import UserUtils, MODULE_CONTEXT
import ast
from anuvaad_auditor.loghandler import log_info, log_exception
from flask import request
from flask import jsonify
from anuvaad_auditor.errorhandler import post_error
import config


class CreateUsers(Resource):

    def post(self):
        body = request.get_json()
        if 'users' not in body or not body['users']:
            return post_error("Data Missing", "users not found", None), 400

        users = body['users']
        log_info("Data received for user creation is:{}".format(users), MODULE_CONTEXT)
        
        for user in users:
            validity = UserUtils.validate_user_input_creation(user)
            log_info("User is validated:{}".format(validity), MODULE_CONTEXT)
            if validity is not None:
                return validity, 400

        try:
            result = UserManagementRepositories.create_users(users)
            
            log_info("User creation result:{}".format(result), MODULE_CONTEXT)
            if result is not None:
                return result, 400
                
            else:
                res = CustomResponse(Status.SUCCESS_USR_CREATION.value, None)
                return res.getresjson(), 200
                

        except Exception as e:
            log_exception("Exception while creating user records: " +
                          str(e), MODULE_CONTEXT, e)
            return post_error("Exception occurred", "Exception while performing user creation:{}".format(str(e)), None), 400


class UpdateUsers(Resource):

    def post(self):
        body = request.get_json()
        if 'users' not in body or not body['users']:
            return post_error("Data Missing", "users not found", None), 400

        users = body['users']
        log_info("Data recieved for user updation is:{}".format(
            users), MODULE_CONTEXT)
        
        for user in users:
            validity = UserUtils.validate_user_input_updation(user)
            log_info("User is validated: {}".format(validity), MODULE_CONTEXT)
            if validity is not None:
                return validity, 400

        try:
            result = UserManagementRepositories.update_users(users)
            log_info("User updation result:{}".format(result), MODULE_CONTEXT)
            if result== True:
                res = CustomResponse(Status.SUCCESS_USR_UPDATION.value, None)
                return res.getresjson(), 200
            else:
                return result, 400

        except Exception as e:
            log_exception("Exception while updating user records: " +
                          str(e), MODULE_CONTEXT, e)
            return post_error("Exception occurred", "Exception while performing user updation:{}".format(str(e)), None), 400


class SearchUsers(Resource):

    def post(self):
        
        userIDs = []
        userNames = []
        roleCodes = []
        orgCodes = []
        offset = None
        limit_value = None
        body = request.get_json()
        if "userIDs" in body:
            userIDs = body['userIDs']
        if "userNames" in body:
            userNames = body['userNames']
        if "roleCodes" in body:
            roleCodes = body['roleCodes']
        if "orgCodes" in body:
            orgCodes = body['orgCodes']
        if "offset" in body:
            offset = body['offset']
        if "limit" in body:
            limit_value = body['limit']
        
        
        
        log_info("data recieved for user search is;user Ids:{}".format(userIDs)+'\n'+"user names:{}".format(userNames) +
                 '\n'+"role codes:{}".format(roleCodes)+
                 '\n'+"org codes:{}".format(orgCodes), MODULE_CONTEXT)
        
        if not userIDs and not userNames and not roleCodes and not orgCodes and not offset and not limit_value:
            offset=config.OFFSET_VALUE
            limit_value=config.LIMIT_VALUE

        try:
            result = UserManagementRepositories.search_users(userIDs, userNames, roleCodes,orgCodes,offset,limit_value)
            log_info("User search result:{}".format(result), MODULE_CONTEXT)
            if result == None:
                res = CustomResponse(
                    Status.EMPTY_USR_SEARCH.value, None)
                return res.getresjson(), 200
            res = CustomResponse(Status.SUCCESS_USR_SEARCH.value, result[0],result[1])
            return res.getresjson(), 200
        except Exception as e:
            log_exception("Exception while searching user records: " +
                          str(e), MODULE_CONTEXT, e)
            return post_error("Exception occurred", "Exception while performing user search:{}".format(str(e)), None), 400


class OnboardUsers(Resource):

    def post(self):
        body = request.get_json()
        if 'users' not in body or not body['users']:
            return post_error("Data Missing", "users not found", None), 400

        users = body['users']
        log_info("Data received for user onboarding is:{}".format(users), MODULE_CONTEXT)


        for user in users:
            validity = UserUtils.validate_user_input_creation(user)
            log_info("User is validated:{}".format(validity), MODULE_CONTEXT)
            if validity is not None:
                return validity, 400

        try:
            result = UserManagementRepositories.onboard_users(users)
            
            log_info("User on-boarding result:{}".format(result), MODULE_CONTEXT)
            if result is not None:
                return result, 400
                
            else:
                res = CustomResponse(Status.SUCCESS_USR_ONBOARD.value, None)
                return res.getresjson(), 200
                

        except Exception as e:
            log_exception("Exception while creating user records for users on-boarding: " +
                          str(e), MODULE_CONTEXT, e)
            return post_error("Exception occurred", "Exception while performing users on-boarding::{}".format(str(e)), None), 400


   

class Health(Resource):
    def get(self):
        response = {"code": "200", "status": "ACTIVE"}
        return jsonify(response)


