
import os
from pdf2image import convert_from_path

def process_pdf_file(pdf_path, output_folder):
    """
    将 PDF 文件转换为图片并保存到指定文件夹
    :param pdf_path: PDF 文件路径
    :param output_folder: 输出图片文件夹
    :return: 图片文件路径列表
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    images = convert_from_path(pdf_path)
    image_paths = []
    
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i + 1}.png")
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
    
    return image_paths


def process_pdf_folder(pdf_folder, output_folder):
    """
    处理文件夹中的所有 PDF 文件，将其转换为图片并进行 OCR 识别
    :param pdf_folder: PDF 文件夹路径
    :param output_folder: 输出图片文件夹
    :param ocr: PaddleOCR 对象
    """
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    image_paths_Group=[]
    
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")
        pdf_path = os.path.join(pdf_folder, pdf_file)
        pdf_output_folder = os.path.join(output_folder, os.path.splitext(pdf_file)[0])
        if not os.path.exists(pdf_output_folder):
            os.makedirs(pdf_output_folder)    
        image_paths = process_pdf_file(pdf_path, pdf_output_folder)
        image_paths_Group= image_paths_Group+image_paths

    return image_paths_Group
