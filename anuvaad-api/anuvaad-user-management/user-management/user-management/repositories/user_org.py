from models import UserOrganizationModel


class UserOrganizationRepositories:

    @staticmethod
    def create_organizations(orgs):
        result = UserOrganizationModel.create_organizations(orgs)
        if result is not None:
            return result
        

    @staticmethod
    def update_organizations(orgs):
        result = UserOrganizationModel.update_orgs_by_orgid(orgs)
        if result is not None:
            return result
        else:
            return True

    @staticmethod
    def search_organizations(org_code):
        result = UserOrganizationModel.get_orgs_by_keys(org_code)
        if result is not None:
            return result
