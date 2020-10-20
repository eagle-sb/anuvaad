from flask_restful import fields, marshal_with, reqparse, Resource
from repositories import UserAuthenticationRepositories
from models import CustomResponse, Status
# from utilities import AppContext
import ast
from anuvaad_auditor.loghandler import log_info, log_exception
from flask import request


class UserLogin(Resource):

    def post(self):
        body = request.get_json()
        userName = body["userName"]
        password = body["password"]

        if not userName or not password:
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            # print(res)
            return res.getresjson(), 400

        try:
            result = UserAuthenticationRepositories.user_login(
                userName, password)
            # print(result)
            if result == False:
                res = CustomResponse(
                    Status.FAILURE_USR_LOGIN.value, None)
                return res.getresjson(), 400

            res = CustomResponse(Status.SUCCESS_USR_LOGIN.value, result)
            return res.getres()
        except Exception as e:
            # print(e)
            # log_exception("SaveSentenceResource ",  AppContext.getContext(), e)
            res = CustomResponse(
                Status.FAILURE_USR_LOGIN.value, None)
            return res.getresjson(), 400


class UserLogout(Resource):

    def post(self):
        body = request.get_json()
        userName = body["userName"]

        if not userName:
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            # print(res)
            return res.getresjson(), 400

        try:
            result = UserAuthenticationRepositories.user_logout(userName)
            # print(result,"in resource")
            if result == False:
                res = CustomResponse(
                    Status.FAILURE_USR_LOGOUT.value, None)
                return res.getresjson(), 400
            else:
                res = CustomResponse(Status.SUCCESS_USR_LOGOUT.value, None)
            return res.getres()
        except Exception as e:
            print(e,"in resource exception")
            # log_exception("SaveSentenceResource ",  AppContext.getContext(), e)
            res = CustomResponse(
                Status.FAILURE_USR_LOGOUT.value, None)
            return res.getresjson(), 400


class AuthTokenSearch(Resource):

    def post(self):
        body = request.get_json()
        token = body["token"]
        # print(token)
        if not token:
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            # print(res)
            return res.getresjson(), 400

        try:
            result = UserAuthenticationRepositories.token_search(token)
            # print(result,"reso")
            if result == False:
                res = CustomResponse(
                    Status.FAILURE_USR_TOKEN.value, None)
                return res.getresjson(), 400
            else:
                res = CustomResponse(Status.SUCCESS_USR_TOKEN.value, result)
            return res.getres()
        except Exception as e:
            # print(e,"resource-except")
            # log_exception("SaveSentenceResource ",  AppContext.getContext(), e)
            res = CustomResponse(
                Status.FAILURE_USR_TOKEN.value, None)
            return res.getresjson(), 400
