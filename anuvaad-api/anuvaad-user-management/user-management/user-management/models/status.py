import enum


class Status(enum.Enum):

    SUCCESS = {'ok': True, 'http': {'status': 200},
               'why': "Request successful"}
    FAILURE_GLOBAL_SYSTEM = {'ok': False, 'http': {'status': 500},
                             'why': 'Request failed,Internal Server Error'}

    SUCCESS_USR_CREATION = {'ok': True, 'http': {'status': 200},
                            'why': "New users were created successfully"}
    FAILURE_USR_CREATION = {'ok': False, 'http': {'status': 400},
                            'why': "On input errors causing failure in user account creation"}

    SUCCESS_USR_UPDATION = {'ok': True, 'http': {'status': 200},
                            'why': "users were updated successfully"}
    
    FAILURE_USR_UPDATION = {'ok': False, 'http': {'status': 400},
                            'why': "On input errors causing failure in user account updation"}

    SUCCESS_USR_SEARCH = {'ok': True, 'http': {'status': 200},
                          'why': "users were searched successfully"}
    EMPTY_USR_SEARCH = {'ok': True, 'http': {'status': 200},
                          'why': "No such users"}

    SUCCESS_USR_LOGIN = {'ok': True, 'http': {'status': 200},
                         'why': "Logged in successfully"}
    FAILURE_USR_LOGIN = {'ok': False, 'http': {'status': 400},
                         'why': "On input errors causing failure in user login"}

    SUCCESS_USR_LOGOUT = {'ok': True, 'http': {'status': 200},
                          'why': "Logged out successfully"}
    FAILURE_USR_LOGOUT = {'ok': False, 'http': {'status': 400},
                          'why': "On input errors causing failure in user logout"}

    SUCCESS_USR_TOKEN = {'ok': True, 'http': {'status': 200},
                         'why': "Search is successful"}
    FAILURE_USR_TOKEN = {'ok': False, 'http': {'status': 400},
                         'why': "On input errors causing failure in user search"}

    SUCCESS_FORGOT_PWD = {'ok': True, 'http': {'status': 200},
                            'why': "User is notified successfully"}
    FAILURE_FORGOT_PWD  = {'ok': False, 'http': {'status': 400},
                         'why': "On input errors causing failure in user notification"}

    SUCCESS_RESET_PWD = {'ok': True, 'http': {'status': 200},
                            'why': "Password has resetted successfully"}
    FAILURE_RESET_PWD  = {'ok': False, 'http': {'status': 400},
                         'why': "On input errors causing failure in password resetting"}
    
    SUCCESS_ACTIVATE_USR = {'ok': True, 'http': {'status': 200},
                            'why': "User has verified/activated successfully"}
    FAILURE_ACTIVATE_USR  = {'ok':False, 'http': {'status': 400},
                         'why': "On input errors causing failure in user activation"}
    
    SUCCESS_USR_ONBOARD = {'ok': True, 'http': {'status': 200},
                            'why': "New users were onboarded successfully"}
    SUCCESS_ORG_CREATION = {'ok': True, 'http': {'status': 200},
                            'why': "New organizations were created successfully"}
    SUCCESS_ORG_UPDATION = {'ok': True, 'http': {'status': 200},
                            'why': "organizations were updated successfully"}

    ERR_GLOBAL_SYSTEM = {'ok': False, 'http': {
        'status': 500}, 'why': "Internal Server Error"}
    ERR_GLOBAL_MISSING_PARAMETERS = {
        'ok': False, 'http': {'status': 400}, 'why': "Data Missing"}

    