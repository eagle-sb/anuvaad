from flask import Blueprint
from flask_restful import Api
from resources import CreateUsers, UpdateUsers, SearchUsers, UserLogin, UserLogout, AuthTokenSearch, Health


USER_MANAGEMENT_BLUEPRINT = Blueprint("user-management", __name__)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    CreateUsers, "/v1/users/create"
)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    UpdateUsers, "/v1/users/update"
)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    SearchUsers, "/v1/users/search"
)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    UserLogin, "/v1/users/login"
)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    UserLogout, "/v1/users/logout"
)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    AuthTokenSearch, "/v1/users/auth-token-search"
)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    Health, "/health"
)