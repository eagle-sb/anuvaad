from flask import Blueprint
from flask_restful import Api
from resources import CreateUsers, UpdateUsers, SearchUsers,OnboardUsers, Health, DeactivateUser
from resources import UserLogin, UserLogout, AuthTokenSearch, ForgotPassword, ResetPassword , ActivateUser, RegisteredUsersRecords


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
    ForgotPassword, "/v1/users/forgot-password"
)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    ResetPassword, "/v1/users/reset-password"
)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    ActivateUser,"/v1/users/activate-user"
)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    DeactivateUser,"/v1/users/deactivate-user"
)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    OnboardUsers,"/v1/users/onboard-users"
)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    RegisteredUsersRecords,"/v1/users/fetch-users-records"
)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    Health, "/health"
)