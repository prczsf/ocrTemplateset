
from flask import  request, jsonify
from flask_restful import Resource
import os,json
import cv2
from paddleocr import PaddleOCR, PPStructure

ocr = {
    'zh': PaddleOCR(use_angle_cls=True, lang='ch'),
    'en': PaddleOCR(use_angle_cls=True, lang='en')
}
table_engine = PPStructure()

class PaddleOfflineOcrView(Resource):
    def post(self):
        json_data = request.form.get('json')
        image_name = request.form.get('image_name')

        if not json_data or not image_name:
            return {'error': 'Invalid input'}, 400

        data = json.loads(json_data)

        image_path = os.path.join('filesPic', image_name, 'page_1.png')
        if not os.path.exists(image_path):
            return {'error': 'Image not found'}, 404

        image = cv2.imread(image_path)
        height, width = image.shape[:2]
        scale = 1080 / width
        image = cv2.resize(image, (1080, int(height * scale)))


        results = []

        for item in data:
            rect_area = eval(item['rectArea'])
            x, y, w, h = [round(float(coord)) for coord in rect_area]
            print(x, y, w, h)
            roi = image[y:y+h, x:x+w]
            cv2.imwrite('temp.png', roi)

            language = item['language']
            ocr_engines = ocr.get(language, ocr['zh'])  # 默认使用中文OCR引擎
            text = ''
            if item['type'] in ['header', 'footer']:
                result = ocr_engines.ocr('temp.png', cls=True)

                try:
                    # text = ''.join(line[1][0] for line in result[0][0])
                    text = ''.join(result[0][0][1][0])

                except:
                    print('error')

            elif item['type'] == 'body':
                # text = 'toBeImplemented'
                try:
                    result = table_engine(roi)
                    text = result[0]['res']["html"]
                except:
                    print('error')

            if text:
                item['rectVarValue'] = text
            results.append(item)

        return jsonify(results)