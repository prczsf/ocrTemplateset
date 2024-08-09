import os
import cv2
import numpy as np
from paddleocr import PPStructure, PaddleOCR

# 初始化PP-Structure和PaddleOCR
table_engine = PPStructure(show_log=False)
ocr = PaddleOCR(use_angle_cls=True)  # 启用方向分类器

rotateTimePerImg=0

def checkImgAndRotate(imgRead, rotate_time=0):
    result = table_engine(imgRead)
    
    for line in result:
        if line['type'] == 'table':
            print("table found!")
            return imgRead, result, rotate_time
    
    if rotate_time < 4:  # Check the rotation limit before rotating
        imgRotated = cv2.rotate(imgRead, cv2.ROTATE_90_CLOCKWISE)
        return checkImgAndRotate(imgRotated, rotate_time + 1)  # Return the recursive call
    else:
        print("table not found!")
        return imgRead, result, rotate_time

def correct_table_image(img_path, output_path):
    # 读取图像
    imgRead = cv2.imread(img_path)
    if imgRead is None:
        print(f"Error: Could not read image from {img_path}")
    
    img, result,rotate_time= checkImgAndRotate(imgRead)
    print(result)
    # 检测表格
   #  if img_path contains fenuangqinghua
    # if 'fenuangqinghua' in img_path:
    #     print(result)
    #     img_rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    #     result = table_engine(img_rotated)

    # 获取表格的四个角点
    for line in result:
        if line['type'] == 'table':
            bbox = line['bbox']
            # print("Table corners:", bbox)

            # 确保bbox包含两个对角点并且是np.float32类型
            if len(bbox) == 4:
                x1, y1, x2, y2 = bbox
                pts1 = np.float32([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
                width = x2 - x1
                height = y2 - y1

                # 目标点
                pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

                # 计算透视变换矩阵
                M = cv2.getPerspectiveTransform(pts1, pts2)

                # 应用透视变换
                dst = cv2.warpPerspective(img, M, (int(width), int(height)))

                # 在dst图像周围添加空白区域50px宽度
                dst = cv2.copyMakeBorder(dst, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=[0, 153, 225])

                # 保存结果
                cv2.imwrite(output_path, dst)
                print(f"Corrected table image saved to {output_path}")
            else:
                print("Error: bbox does not contain exactly 4 points.")

def process_images_in_folder(img_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有图像文件
    for filename in os.listdir(img_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(img_folder, filename)
            print(f"Processing image: {img_path}")
            output_path = os.path.join(output_folder, filename)
            correct_table_image(img_path, output_path)

if __name__ == "__main__":
    img_folder = 'image_folder'
    output_folder = 'output_folder'
    process_images_in_folder(img_folder, output_folder)
