import API from "./api";
import C from "../constants";
import ENDPOINTS from "../../../configs/apiendpoints";

export default class RunExperiment extends API {


  constructor(workflow, file, fileName, source, target, path, model, timeout = 2000) {

    super("POST", timeout, false);
    this.type = C.WORKFLOW;
    this.file = file;
    this.fileName = fileName;
    this.endpoint = workflow  === "WF_A_FCBMTKTR" ? `${super.apiEndPointAuto()}${ENDPOINTS.workflowAsync}`: `${super.apiEndPointAuto()}${ENDPOINTS.workflowSync}`
    this.source = source;
    this.target = target;
    this.path = path;
    this.model = model;
    this.workflow = workflow;

  }

  toString() {
    return `${super.toString()} , type: ${this.type}`;
  }

  processResponse(res) {
    super.processResponse(res);

    if (res) {
      this.sentences = res;

    }
  }

  apiEndPoint() {
    return 'https://poczuul.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/async/initiate';
  }

  getBody() {
    if (this.workflow === "WF_A_FCBMTKTR") {
      return {

        "workflowCode":"WF_A_FCBMTKTR","jobName":"31.01.2020.pdf","files":[{"path":"30c789c8-116d-44a1-b5e6-18812a437895.pdf","type":"pdf","locale":"en","model":{"_id":"5d7f7b184dc7f557106e8dce","source_language_code":"en","target_language_code":"bn","model_id":11,"model_name":"model no-1:","is_primary":true,"created_on":"2019-09-16T12:07:52.645Z","deployed_on":"2019-09-16","status":"ACTIVE","url_end_point":"translate-anuvaad","interactive_end_point":"interactive-translation"}}]

      //   "workflowCode": this.workflow,
      //   "jobName": this.fileName,
      //   "files": [
      //     {
      //       "path": this.file,
      //       "type": this.path,
      //       "locale": this.source,
      //       "model": this.model
      //     }
      //   ]

       };
    }
    else if (this.workflow === "WF_S_TKTR" ||this.workflow === "WF_S_TR") {
      return {
        "workflowCode": this.workflow,
  "recordID":this.fileName,
  "locale":this.source, // Only when tokenisation and/or translation is needed
  "modelID":this.model, //Only when Translation is needed
  "textBlocks":this.file
      }
      //List of text 
    }

  }

  getHeaders() {
    this.headers = {
      headers: {
        Authorization: `Bearer ${decodeURI(localStorage.getItem("token"))}`,
        "Content-Type": "application/json"
      }
    };
    return this.headers;
  }

  getPayload() {
    return this.sentences;
  }
}