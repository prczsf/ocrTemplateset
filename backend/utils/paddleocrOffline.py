from pdf2image import convert_from_path
from paddleocr import PPStructure, save_structure_res
import cv2, os

def paddlePP_table_recognition(image_path, table_engine):
    """
    对图片进行表格识别
    :param image_path: 图片文件路径
    :param table_engine: PaddleOCR 表格识别引擎
    :return: 表格识别结果
    """
    image = cv2.imread(image_path)
    result = table_engine(image)
    return result

def paddlePP_save_table_results(results, output_folder, image_name):
    """
    将表格识别结果保存到文件
    :param results: 表格识别结果
    :param output_folder: 输出文件夹
    :param image_name: 图片文件名
    """
    image_name ='ocr_'+image_name
    save_structure_res(results, output_folder, image_name)

if __name__ == '__main__':
    pdf_folder = './exampdf/pdf'
    output_folder = './exampdf/output'
    image_path = './exampdf/pdf/1.jpg'
    table_engine = PPStructure(show_log=True)
    result = paddlePP_table_recognition(image_path, table_engine)
    paddlePP_save_table_results(result, output_folder, os.path.basename(image_path))

