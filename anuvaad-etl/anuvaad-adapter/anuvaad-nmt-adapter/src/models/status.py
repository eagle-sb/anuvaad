import enum


class Status(enum.Enum):
    
    SUCCESS = { "statusCode": 200 , "message": "Requested operation successful" }
    OUT_OF_RANGE = {"statusCode": 401 , "message": "Length of list is limit to 25 only" }
    ID_MISSING = {"statusCode": 404 , "message": "No ID found in the request" }
    LANGUAGE_MISSING = {"statusCode": 404 , "message": "No language found in the request" }
    MANDATORY_PARAM_MISSING = {"statusCode": 401 , "message": "missing mandatory input parameters: src_phrases or tgt" }
    TYPE_OR_LANGUAGE_MISSING = {  "statusCode": 404 , "message": "either type or language missing in form data" }
    INVALID_TYPE = {"statusCode": 401 , "message": "Invalid file type of file to be downloaded/uploaded !" }
    SYSTEM_ERR = {"statusCode": 500 , "message": "Something went wrong on the server !" }
    SEVER_MODEL_ERR = {"statusCode": 500 , "message": "Something went wrong on the server !" }
    UNSUPPORTED_LANGUAGE = {"statusCode": 401 , "message": "only hindi and english languages are supported" }
    No_File_DB = {"statusCode": 401 , "message": "no file found in the db for the given id" }
    ID_OR_SRC_MISSING = {"statusCode": 401 , "message": "Either id or src missing for some inputs in the request" }
    INCORRECT_ID = {"statusCode": 401 , "message": "wrong model id for some input" }
    INVALID_API_REQUEST = {"statusCode": 401 , "message": "invalid api request,either incorrect format or empty request"}
    INCOMPLETE_API_REQUEST = {"statusCode": 401 , "message": "Mandatory input parameters missing" }