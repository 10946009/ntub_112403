from PIL import Image
import os

def crop_to_4_3(image_path,name):
    # 打开图像
    img = Image.open(image_path)

    # 获取图像的宽度和高度
    width, height = img.size

    # 计算目标裁切区域的宽度和高度
    target_width = min(width, height * 4 // 3)
    target_height = min(height, width * 3 // 4)

    # 计算目标裁切区域的左上角和右下角坐标
    left = (width - target_width) // 2
    top = (height - target_height) // 2
    right = left + target_width
    bottom = top + target_height

    # 裁切图像
    cropped_img = img.crop((left, top, right, bottom))

    # 保存裁切后的图像（可选）
    cropped_img.save(name)

    return cropped_img

# 示例用法
for i in os.listdir():
    if '.jpg' not in i: continue
    image_path = f"{os.getcwd()}\\{i}"  # 替换为要裁切的图片路径
    cropped_image = crop_to_4_3(image_path,i)
    # cropped_image.show()  # 显示裁切后的图像

