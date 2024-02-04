# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '视频加工躲避检测'

import hashlib
from moviepy.editor import *


# 获取文件的MD5值
def get_file_md5(in_path):
    with open(in_path, 'rb') as file:
        temp_md5 = hashlib.md5()
        temp_md5.update(file.read())
        hash_code = str(temp_md5.hexdigest()).lower()
    return hash_code


# 修改文件的md5值
def modify_file_md5(in_path):
    with open(in_path, 'a') as file:
        file.write("####&&&&")


# 分段读取，获取文件的md5值
def get_file_md5_2(in_path):
    with open(in_path, 'rb') as file:
        md5_obj = hashlib.md5()
        while True:
            buffer = file.read(8096)
            if not buffer:
                break
            md5_obj.update(buffer)
        hash_code = md5_obj.hexdigest()
    md5 = str(hash_code).lower()
    return md5


# 处理图片帧
def handle_frame(image_frame):
    image_frame_result = image_frame * 1.12
    # 如果颜色值超过255，直接设置为255
    image_frame_result[image_frame_result > 255] = 255
    return image_frame_result


# 增加视频整体亮度
def increase_video_brightness(in_path):
    video = VideoFileClip(in_path)
    result = video.fl_image(handle_frame)

    out_path = "result_video/CNN色彩调整.mp4"
    result.write_videofile(out_path)


# 增加视频整体亮度2
def increase_video_brightness2(in_path):
    # 调整系数值
    coefficient_value = 1.019
    video = VideoFileClip(in_path)

    out_path = "result_video/CNN色彩调整.mp4"
    video.fx(vfx.colorx, coefficient_value).write_videofile(out_path)


# 降低亮度
def decrease_video_brightness(in_path):
    # 调整系数值
    coefficient_value = 0.89
    video = VideoFileClip(in_path)

    out_path = "result_video/RNN色彩调整.mp4"
    video.fx(vfx.colorx, coefficient_value).write_videofile(out_path)


# 黑白处理
def change_video_bhd(in_path):
    video = VideoFileClip(in_path)

    out_path = "result_video/视频二值化处.mp4"
    video.fx(vfx.blackwhite).write_videofile(out_path)


# 先获取图片帧，单张进行处理，然后合成
def change_video_todo(in_path):
    pass


def process_function_1(in_path):
    # print(get_file_md5_2(in_path))
    # 修改MD5
    modify_file_md5(in_path)
    # print(get_file_md5_2((in_path))

    # 亮度处理
    # increase_video_brightness(in_path)
    increase_video_brightness2(in_path)

    # 降低亮度
    # decrease_video_brightness(in_path)

    # 饱和度处理
#     change_video_bhd(in_path)
