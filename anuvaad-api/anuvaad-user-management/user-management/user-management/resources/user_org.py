from flask_restful import fields, marshal_with, reqparse, Resource
from repositories import UserOrganizationRepositories
from models import CustomResponse, Status
from utilities import OrgUtils, MODULE_CONTEXT
import ast
from anuvaad_auditor.loghandler import log_info, log_exception
from flask import request
from flask import jsonify
from anuvaad_auditor.errorhandler import post_error
import config

orgRepo = UserOrganizationRepositories()

class CreateOrganization(Resource):

    def post(self):
        body = request.get_json()
        if 'organizations' not in body.keys():
            return post_error("Key error", "organizations not found", None), 400

        if 'organizations' in body:
            organizations = body['organizations']
        log_info("data recieved for organization creation is:{}".format(
            organizations), MODULE_CONTEXT)
        if not organizations:
            return post_error("Data Null", "data received for org creation is empty", None), 400

        orgcodes=[]
        for i,org in enumerate(organizations):
            validity = OrgUtils.validate_org_upsert(i,org)
            log_info("Org is validated:{}".format(validity), MODULE_CONTEXT)
            if validity is not None:
                return validity, 400
            orgcodes.append(str(org["code"]).upper())
        if (len(organizations) != len(set(orgcodes))):
            return post_error("Duplicate org code","Org codes should be unique",None), 400

        try:
            result = orgRepo.create_organizations(organizations)
            
            log_info("Org creation result:{}".format(result), MODULE_CONTEXT)
            if result is not None:
                if result[1]==True:
                    res = CustomResponse(Status.SUCCESS_ORG_CREATION.value, None)
                    return res.getresjson(), 200
                if result[1]==False:
                    res = CustomResponse(Status.SUCCESS_ORG_DEACTIVATE.value, None)
                    return res.getresjson(), 200
                else:
                    return result, 400
                

        except Exception as e:
            log_exception("Exception while creating organization records: " +
                          str(e), MODULE_CONTEXT, e)
            return post_error("Exception occurred", "Exception while performing organization creation:{}".format(str(e)), None), 400




class SearchOrganization(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('org_code', type=str, location='args', help='organization code to be searched', required=False)
        args    = parser.parse_args()
        org_code=args["org_code"]
        try:
            result = orgRepo.search_organizations(org_code)
            log_info("User search result:{}".format(result), MODULE_CONTEXT)
            if result == None:
                res = CustomResponse(
                    Status.EMPTY_ORG_SEARCH.value, None)
                return res.getresjson(), 400
            res = CustomResponse(Status.SUCCESS_ORG_SEARCH.value, result)
            return res.getresjson(), 200
        except Exception as e:
            log_exception("Exception while searching user records: " +
                          str(e), MODULE_CONTEXT, e)
            return post_error("Exception occurred", "Exception while performing user search::{}".format(str(e)), None), 400



