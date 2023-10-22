import os

def get_picture_list(placeid):
    # 使用os.path.normpath()来规范化路径，以确保路径分隔符和斜杠方向的一致性
    path = os.path.join(os.getcwd(), "static", "images", "attractions")
    path = os.path.normpath(path)
    # 使用os.listdir()来列出目录中的文件
    file_list = os.listdir(path)
    filtered_list = [item for item in file_list if placeid in item]
    return filtered_list