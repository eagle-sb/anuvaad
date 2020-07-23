import json
import requests
from utilities.ptf_to_html_integration import pdf_to_json ,add_width_and_line


ocr_api = 'https://auth.anuvaad.org/api/v3/ocr/lines'



def post_request(url ,param):
    param = json.dumps(param)
    headers = {"Content-Type": "application/json"}
    #print(param)
    r = requests.post(url, data = param , headers=headers )
    return r.json()

def get_iou(bb1, bb2):
    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou

def cal_iou_score(html_data, ocr_data,iou_threshold=0.7):
    for page in html_data:
        w = ocr_data['resolution']['x']
        h = ocr_data['resolution']['y']
        for num, line in enumerate(html_data[str(page)]['html_nodes']):

            width_ratio = float(w / int(line['page_width']))
            height_ratio = float(h / int(line['page_height']))
            left = int(width_ratio * int(line['x']))
            top = int(height_ratio * int(line['y']))
            bottom = int(height_ratio * int(line['bottom']))#top + int(height_ratio * int(line['class_style']['font-size'][:-2]))
            right =  int(width_ratio * int(line['right']))#left + int(int(line['class_style']['font-size'][:-2]) * len(line['text']))
            page_no = int(line['page_no'])
            bb1 = {'x1': left, 'y1': top, 'x2': right, 'y2': bottom}
            total_score = 0
            top_3_iou = []
            visual_break = 0
            line['ocr_width']  = None

            for ocr_line in ocr_data['lines_data'][page_no - 1]['line_data']:
                ocr_left = ocr_line['left']
                ocr_right = ocr_line['right']
                ocr_top = ocr_line['top']
                ocr_bottom = ocr_line['bottom']
                bb2 = {'x1': ocr_left, 'y1': ocr_top, 'x2': ocr_right, 'y2': ocr_bottom}

                iou = get_iou(bb1, bb2)

                top_3_iou.append(iou)
                if iou >= 0.1:
                    #print("iou", iou)
                    #print("total_score", total_score)
                    total_score = total_score + iou * ocr_line['visual_break']
                    #visual_break = ocr_line['visual_break']

                if iou >= 0.5:
                    line['ocr_width'] = int(ocr_line['widht'] / width_ratio)
                    #right = ocr_right

                #else :

            line['iou_score'] = total_score
            top_3_iou_sorted = sorted(top_3_iou, reverse=True)
            line['top_iou'] = top_3_iou_sorted[0]
            if  line['top_iou'] >= iou_threshold:
                line['visual_break'] = 1 #int(visual_break)
            #line['right'] = right
            # print(line['top_3_iou'])
            html_data[str(page)]['html_nodes'][num] = line

    return html_data



def pdf_html_with_vbs(file_id):
    param = {"pdf_file_id":file_id}

    html_data = pdf_to_json(file_id)
    html_data =  add_width_and_line(html_data)

    ocr_data = post_request(ocr_api,param)

    html_data = cal_iou_score(html_data, ocr_data)
    return html_data
# input_image_path = "/home/naresh/Tesseract/sentence_extraction/hw-recog-be/src/tmp/images/167_2009_11_1501_16003_Judgement_14-Aug-2019/0001-1.jpg"
# ​
#
# def draw_bounding_box(filepath, html_data, page_no):
#     image = Image.open(filepath)
#     draw = ImageDraw.Draw(image)
#     w = image.size[0]
#     h = image.size[1]
#     for line in html_data[str(page_no)]['html_nodes']:
#         width_ratio = float(w / int(line['page_width']))
#         height_ratio = float(h / int(line['page_height']))
#         left = int(width_ratio * int(line['x']))
#         top = int(height_ratio * int(line['y']))
#         line_height = int(height_ratio * int(line['class_style']['font-size'][:-2]))
#         bottom = top + line_height
#         # right = w-30
#         font_size = int(line['class_style']['font-size'][:-2])
#         # width of the line
#         right = left + int(int(line['class_style']['font-size'][:-2]) * len(line['text']))
#         # right = left+int(font_size*len(line['text']))
#         if line["visual_break"]:  # and line['iou_score']>0.40
#             draw.rectangle(((left, top), (right, bottom)), outline="red")
#         else:
#             draw.rectangle(((left, top), (right, bottom)), outline="green")
#         #
#     return image
#
#
# input_image1 = draw_bounding_box(input_image_path, html_data, 0)
# input_image1
# ​
# ​
# # In[43]:
# ​
# ​
# ​
#
# def draw_bounding_box_ocr(filepath, ocr_data, page_no):
#     w = ocr_data['resolution'][0]['x']
#     h = ocr_data['resolution'][0]['y']
#     image = Image.open(filepath)
#     draw = ImageDraw.Draw(image)
#     for ocr_line in ocr_data['lines_data'][page_no - 1]['line_data']:
#         left = ocr_line['left']
#         right = ocr_line['right']
#         top = ocr_line['top']
#         bottom = ocr_line['bottom']
#         if ocr_line['visual_break']:
#             draw.rectangle(((left, top), (right, bottom)), outline="red")
#         else:
#             draw.rectangle(((left, top), (right, bottom)), outline="green")
#         # cv2.rectangle(input_image, (left,top), (right,bottom), (0), 2)
#     return image
#
#
# input_image1 = draw_bounding_box_ocr(input_image_path, ocr_data, 1)
# input_image1
# ​
# ​
# # In[ ]:
