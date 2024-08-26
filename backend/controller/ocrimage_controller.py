
from flask import  request, jsonify
from flask_restful import Resource
import cv2
from paddleocr import PaddleOCR, PPStructure
from paddleocr.ppstructure.recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx
from flask_restful import Resource
import numpy as np


class OCR2:
    ppstructure = PPStructure()

    def __init__(self):
        # self.ppstructure = PPStructure(show_log=False, recovery=True, lang='en', layout=True, structure_version='PP-StructureV2')
        self.ppstructure = PPStructure()

    def get_res(self, bytes):
        img = cv2.imdecode(np.frombuffer(bytes, dtype=np.uint8), 1)
        result = self.ppstructure(img)
        
        h, w, _ = img.shape  # 记录图片的形状
        res = sorted_layout_boxes(result, w)
        for item in res:
            del item['img']
        print(res)
        
        return {
            'imgShape': {
                'h': h,
                'w': w
            },
            'res': res
        }
ocr_engine = OCR2()

class OCRImageView(Resource):
    def post(self):
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.content_type.count('image') != 0:
            result = ocr_engine.get_res(file.read())
            return jsonify(result)
        else:
            return 'No image file', 400