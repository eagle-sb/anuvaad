
MODULE_CONTEXT = {'metadata': {'module': 'USER-MANAGEMENT','userID':None,'userName':None}}


def init():
    global app_context
    app_context = {
        'application_context': None
    }
# class AppContext:
def addUserID(userID):
    if userID is not None:
        MODULE_CONTEXT['metadata']['userID']=userID

def adduserName(userName):
    if userName is not None:
        MODULE_CONTEXT['metadata']['userName']=userName