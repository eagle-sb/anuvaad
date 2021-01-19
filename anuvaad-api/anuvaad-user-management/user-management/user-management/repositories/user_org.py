from models import UserOrganizationModel


class UserOrganizationRepositories:

    @staticmethod
    def create_organizations(orgs):
        result = UserOrganizationModel.create_organizations(orgs)
        if result is not None:
            return result
        

    @staticmethod
    def search_organizations(org_code):
        result = UserOrganizationModel.get_orgs_by_keys(org_code)
        if result is not None:
            return result
