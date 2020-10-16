import enum


class Status(enum.Enum):

    SUCCESS = {'ok': True, 'http': {'status': 200},
               'why': "Request successful"}
    FAILURE_GLOBAL_SYSTEM = {'ok': False, 'http': {'status': 500},
               'why': 'Request failed,Internal Server Error'}

    SUCCESS_USR_CREATION=  {'ok': True, 'http': {'status': 200},
               'why': "New users were created successfully"} 
    FAILURE_USR_CREATION={'ok': True, 'http': {'status': 400},
               'why': "On input errors causing failure in user account creation"} 

    SUCCESS_USR_UPDATION=  {'ok': True, 'http': {'status': 200},
               'why': "users were updated successfully"}  
    FAILURE_USR_UPDATION=  {'ok': True, 'http': {'status': 400},
               'why': "On input errors causing failure in user account updation"} 

    SUCCESS_USR_SEARCH=  {'ok': True, 'http': {'status': 200},
               'why': "users were updated successfully"}  
    FAILURE_USR_SEARCH=  {'ok': True, 'http': {'status': 400},
               'why': "On input errors causing failure in user account updation"} 

    SUCCESS_USR_LOGIN=  {'ok': True, 'http': {'status': 200},
               'why': "Logged in successfully"} 
    FAILURE_USR_LOGIN={'ok': True, 'http': {'status': 400},
               'why': "On input errors causing failure in user login"}



    ERR_GLOBAL_SYSTEM = {'ok': False, 'http': {
        'status': 500}, 'why': "Internal Server Error"}
    ERR_GLOBAL_MISSING_PARAMETERS = {
        'ok': False, 'http': {'status': 400}, 'why': "Data Missing"}

    ERR_MANDATORY_FIELDS_MISSING= {
        'ok': False, 'http': {'status': 400}, 'why': "Username, Password, Email and Phone number are mandatory fields.they cannot be empty"}
    FAILURE = {'ok': False, 'http': {'status': 500},
               'why': 'request failed'}
    CORRUPT_FILE = {'ok': False, 'http': {'status': 500},
                    'why': 'uploaded file is corrupt'}
    DATA_NOT_FOUND = {'ok': False, 'http': {'status': 404},
                      'why': 'data not found'}
    OPERATION_NOT_PERMITTED = {'ok': False, 'http': {'status': 400},
                               'why': 'operation not permitted'}
    ERROR_WEAK_PASSWORD = {'ok': False, 'http': {
        'status': 400}, 'why': 'weak password, at least provide 6 characters '}
    ERROR_GATEWAY = {'ok': False, 'http': {
        'status': 400}, 'why': 'gateway error'}
    ERROR_UNSUPPORTED_FILE = {'ok': False, 'http': {
        'status': 400}, 'why': 'unsupported file'}
    ERROR_NOTFOUND_FILE = {'ok': False, 'http': {
        'status': 400}, 'why': 'file not found'}
    ERROR_WRONG_PASSWORD = {'ok': False, 'http': {
        'status': 400}, 'why': 'wrong password '}
    USER_ALREADY_EXISTS = {'ok': False, 'http': {
        'status': 400}, 'why': 'username already exists '}
