from flask import Blueprint
from flask_restful import Api
from resources import CreateOrganization, UpdateOrganization, SearchOrganization

ORGANIZATION_BLUEPRINT = Blueprint("organization", __name__)

Api(ORGANIZATION_BLUEPRINT).add_resource(
    CreateOrganization, "/v1/organization/create"
)

Api(ORGANIZATION_BLUEPRINT).add_resource(
    UpdateOrganization, "/v1/organization/update"
)

Api(ORGANIZATION_BLUEPRINT).add_resource(
    SearchOrganization, "/v1/organization/search"
)