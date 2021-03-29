from flask_restful import Resource
from flask import request
from models import CustomResponse, Status
from utilities import MODULE_CONTEXT
from anuvaad_auditor.loghandler import log_info, log_exception
import config
import json 
import os
from google.cloud import translate
from google.protobuf.json_format import MessageToDict
import uuid

class GoogleTranslate_v3(Resource):
    def post(self):
        try:
            project_id = config.PROJECT_ID
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.CREDENTIALS
            client = translate.TranslationServiceClient()
            parent = f"projects/{project_id}"
            body = request.json
            if bool(body) and bool(body['source_language_code']) and bool(body['target_language_code']):
                jsn = body['src_list']
                if len(jsn)>0:
                    val_src =  [li['src'] for li in jsn]
                    response = client.translate_text(request={
                            "parent": parent,
                            "contents": val_src,
                            "mime_type": "text/plain",
                            "source_language_code": body["source_language_code"],
                            "target_language_code": body["target_language_code"]
                        })
                    res = MessageToDict(response._pb)
                    result = []
                    a = res['translations']
                    for value in range(len(a)) and range(len(jsn)):
                        mod_id = {
                                "src":jsn[value]["src"],
                                "s_id":jsn[value]["s_id"],
                                "tgt": a[value]['translatedText']
                        }
                        for k in jsn:
                            k.update(mod_id)
                            result.append(k)
                            out = CustomResponse(Status.SUCCESS.value,result)
                        return out.getres()
            else:
                out = CustomResponse(Status.INVALID_API_REQUEST.value,request.json)
                return out.getres()
        except Exception as e:
                status = Status.SYSTEM_ERR.value
                status['why'] = str(e)
                out = CustomResponse(status, request.json)                  
                return out.getres()