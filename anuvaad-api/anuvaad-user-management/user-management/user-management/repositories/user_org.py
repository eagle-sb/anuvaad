from models import UserOrganizationModel


class UserOrganizationRepositories:
    def __init__(self):
        self.orgModel = UserOrganizationModel()

    
    def create_organizations(self,orgs):
        result = self.orgModel.create_organizations(orgs)
        if result is not None:
            return result
        

    
    def search_organizations(self,org_code):
        result = self.orgModel.get_orgs_by_keys(org_code)
        if result is not None:
            return result
