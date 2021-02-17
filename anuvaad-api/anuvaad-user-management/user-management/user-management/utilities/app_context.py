
MODULE_CONTEXT = {'metadata': {'module': 'USER-MANAGEMENT','userID':None,'userName':None}}

class AppContext:
    @staticmethod
    def addUserID(userID):
        if userID is not None:
            MODULE_CONTEXT['metadata']['userID']=userID
    @staticmethod
    def adduserName(userName):
        if userName is not None:
            MODULE_CONTEXT['metadata']['userName']=userName