import requests
import json


pdf_to_html = 'https://auth.anuvaad.org/api/v0/pdf-to-html'
htm_to_json = 'https://auth.anuvaad.org/api/v0/html-to-json'

file_id = '0018022427'



def post_request(url ,param):
    param = json.dumps(param)
    headers = {"Content-Type": "application/json"}
    print(param)
    r = requests.post(url, data = param , headers=headers )
    return r.json()


pdf_to_html_input = {"input": {"files":[{ "locale": "en","path": file_id,"type": "pdf"}]},"jobID": "Pdf-12354687954","state": "INITIATED","status": "STARTED","stepOrder": 0,"workflowCode": "DP_WFLOW_P","tool":"PDF2HTML"}
phml = post_request(pdf_to_html,pdf_to_html_input)
path_to_html = phml['output']['files'][0]['outputHtmlFilePath']
htm_to_json_input = {"input": {
        "files": [
            {
                "locale": "en",
                "htmlFolderPath": path,
                "imageFolderPath" : "",
                "type": "folder"
            }
        ]},
        "jobID": "HTML2JSON-15913540488115873",
        "state": "INITIATED",
        "status": "STARTED",
        "stepOrder": 0,
        "workflowCode": "DP_WFLOW_p",
        "tool":"HTML2JSON"
    }
pdf_json = post_request(htm_to_json,htm_to_json_input)
print(pdf_json)
print(file_id)
json_path = pdf_json['output']['files'][0]['outputHtml2JsonFilePath']