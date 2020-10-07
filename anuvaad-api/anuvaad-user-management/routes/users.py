from flask import Blueprint
from flask_restful import Api

from resources import CreateUser, UpdateUser, SearchUser

USER-MANAGEMENT_BLUEPRINT = Blueprint("user-management", __name__)

Api(USER-MANAGEMENT_BLUEPRINT).add_resource(
    CreateUser, "/create"
)

Api(USER-MANAGEMENT_BLUEPRINT).add_resource(
    UpdateUser, "/update"
)

Api(USER-MANAGEMENT_BLUEPRINT).add_resource(
    SearchUser, "/search"
)