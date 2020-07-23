import requests
import json
import pandas as pd


pdf_to_html = 'https://auth.anuvaad.org/api/v0/pdf-to-html-wf'
htm_to_json = 'https://auth.anuvaad.org/api/v0/html-to-json-wf'
# param = {"pdf_file_id":"1.pdf"}

file_id = '0018022427'



def post_request(url ,param):
    param = json.dumps(param)
    headers = {"Content-Type": "application/json"}
    #print(param)
    r = requests.post(url, data = param , headers=headers )
    return r.json()

def pdf_to_json(file_id, pdf_to_html=pdf_to_html,  htm_to_json=htm_to_json):
    pdf_to_html_input = {"input": {"files":[{ "locale": "en","path": file_id,"type": "pdf"}]},"jobID": "Pdf-12354687954","state": "INITIATED","status": "STARTED","stepOrder": 0,"workflowCode": "DP_WFLOW_P","tool":"PDF2HTML"}
    phml = post_request(pdf_to_html,pdf_to_html_input)
    print(phml,'dgdg')
    path_to_html = phml['output'][0]['outputHtmlFilePath'] # ['output'][0]['outputHtmlFilePath']


    htm_to_json_input = {"input": {
            "files": [
                {
                    "locale": "en",
                    "htmlFolderPath": path_to_html,
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

    json_path = pdf_json['output'][0]['outputHtml2JsonFilePath']
    #print(json_path)
    pages_count = len(json_path.keys())

    # response = []
    # for i in range(pages_count):
    #     response.append(json_path[str(i)])
    #     #print(json_path[str(i)])

    return json_path

def add_metadata(page_df):
    page_df['y'] = page_df['y'].astype('int32')
    page_df['x'] = page_df['x'].astype('int32')
    page_df['height'] = page_df['class_style'].apply(lambda x: int(x['font-size'][:-2]))
    page_df['bottom'] = page_df['y'] + page_df['height']
    page_df['width'] = page_df['height'] * page_df['text'].str.len()
    page_df['right'] = page_df['x'] + page_df['width']
    page_df = page_df.sort_values(by=['y'])
    page_df['line_index'] = None

    #page_df['height'] = page_df['height'] .astype('int32')

    return page_df

def sort_and_merge_p(group, sorted_group=[], line_spacing=[], line=0):
    semi_height = group.iloc[0]['height'] # / 2.0
    check_y = group.iloc[0]['y']
    same_line = group[abs(group['y'] - check_y) < semi_height]
    next_lines = group[abs(group['y'] - check_y) >= semi_height]
    sort_lines = same_line.sort_values(by=['x'])
    sort_lines['line_index'] = int(line)
    line_spacing.append(same_line['y'].mean())
    line += 1

    for index, row in sort_lines.iterrows():
        sorted_group.append(row)

    if len(next_lines) > 0:
        sort_and_merge_p(next_lines, sorted_group, line_spacing, line)

    return sorted_group, line_spacing, line



def add_width_and_line(html_data):
    line_index = 0
    for page in html_data:
        page_df = pd.DataFrame(html_data[str(page)]['html_nodes'])
        page_df = add_metadata(page_df)

        #sorted_df ,_, line_index = sort_and_merge_p(page_df,[],[],line=line_index )
        html_data[str(page)]['html_nodes'] =page_df.to_dict('records')  # pd.DataFrame(sorted_df).to_dict('records')

    return html_data

