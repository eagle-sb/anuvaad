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
            source_list = {
                'src_list':[{ }],
            }
            j = body['src_list']
            if (len(j))>0 and (len(j))<50:
                val_src =  [li['src'] for li in j]
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
                b = body['src_list']
                for value in range(len(a)) and range(len(b)):
                    mod_id = {
                            "src":b[value]["src"],
                            "s_id":b[value]["s_id"],
                            "tgt": a[value]['translatedText'],
                            "n_id": b[value]["n_id"],
                            "tmx_phrases":b[value]["tmx_phrases"]
                    }
                    result.append(mod_id)
                    out = CustomResponse(Status.SUCCESS.value,result)
                return out.getres()
        except Exception as e:
                status = Status.SYSTEM_ERR.value
                status['why'] = str(e)
                out = CustomResponse(status, None)                  
                return out.getresjson(),500