from flask import Blueprint
from flask_restful import Api
from resources import CreateUsers, UpdateUsers, SearchUsers

USER_MANAGEMENT_BLUEPRINT = Blueprint("user-management", __name__)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    CreateUsers, "/create"
)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    UpdateUsers, "/update"
)

Api(USER_MANAGEMENT_BLUEPRINT).add_resource(
    SearchUsers, "/search"
)
