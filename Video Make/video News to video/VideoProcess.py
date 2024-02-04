# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '合成视频的处理方法'

from moviepy.editor import *
import subprocess
import cv2
import numpy as np
from PIL import Image
from random import choice


"""定义图片的移动方式"""
# 纵向图片向上移动  'center','top'
def VerticalImageUp(image_speed):
    fl = lambda gf, t: gf(t)[int(image_speed * t):int(image_speed * t) + 720, :]
    return fl, ('center', 'top')

# 纵向图片向左移动  'center','top'
def VerticalImageLeft(image_speed):
    fl = lambda gf, t: gf(t)[:, int(image_speed * t):int(image_speed * t) + 720]
    return fl, ('center', 'top')

# 横向图片向上移动  'center','top'
def HorizontalUp(image_speed):
    fl = lambda gf, t: gf(t)[int(image_speed * t):int(image_speed * t) + 720, :]
    return fl, ('center', 'top')

# 横向图片向左移动  'center','top'
def HorizontalLeft(image_speed):
    fl = lambda gf, t: gf(t)[:, int(image_speed * t):int(image_speed * t) + 1280]
    return fl, ('center', 'top')


"""根据制作好的cover.jpg生成封面视频"""
def MakeCoverVideoAndTitle(title, font_path):
    start_time = 0
    duration_time = 0.1

    # 封面视频添加title
    # 将字幕处理成2行
    title_len = int(len(title) / 15)
    title_num = 0
    while title_num <= title_len:
        if title_num == 0:
            strs = title[:(title_num + 1) * 15] + "\n"
        else:
            strs = strs + title[title_num * 15:(title_num + 1) * 15] + "\n"
        title_num = title_num + 1
    title_result = strs

    # 视频添加文字
    txt_clip = (
        TextClip(title_result, font=font_path, fontsize=55, color='white', method='label')
            .set_position(("center", "top"))
            .set_duration(duration_time)
            .set_start(start_time)
    )

    # 视频添加封面
    jpg_path = "./materials/" + title + "/data/cover.jpg"
    image_clip = (
        ImageClip(jpg_path)
            .set_duration(duration_time)
            .set_start(start_time)
    )

    cvc = CompositeVideoClip([image_clip, txt_clip], size=(1280, 720))  # 因为图层 先放图片后放文字
    cvc.write_videofile("./materials/" + title + "/data/cover.mp4", fps=60, remove_temp=False)


"""背景视频中添加轮播图片、字幕、音频解说合成"""
def CompositeVideo(title, mp3_duration, jpg_list, font_path, strs_list, logo_path, cover_mp4, strat_mp4, end_mp4):
    # 处理图片
    start_time = 0  # 设置图片合成视频的起始时间
    image_list = []  # 设置图片处理效果后的结果集合
    image_speed = 10  # 设置图片移动的速度
    jpg_list.remove("cover.jpg")  # 移除定义好的cover.jpg
    for num in range(len(jpg_list[:])):
        # 获取该字段字符串
        words = jpg_list[num]
        # 每段字幕时长
        every_part_duration_time = mp3_duration / len(jpg_list)
        # 图片数据路径
        jpg_path = "./materials/" + title + "/clean_jpg/" + jpg_list[num]
        # 读取图片数据
        img = Image.open(jpg_path)
        # 图片高度和宽度后面进行判断使用
        w, h = img.size[0], img.size[1]
        # 图片移动的速度

        # 这里要判断图片的尺寸执行对应的移动函数
        if w > h:  # 高度 > 宽度 认定图片是纵向图片 横图
            fl, set_pos = choice([HorizontalUp(image_speed),  # 横向图片向上移动
                                  HorizontalLeft(image_speed)])  # 横向图片向左移动
        else:  # 高度 < 宽度 认定图片是横向图片
            fl, set_pos = choice([VerticalImageUp(image_speed),  # 纵向图片向上移动
                                  VerticalImageLeft(image_speed)])  # 纵向图片向左移动
        # 构建每个图片的移动规则
        clip_image = (
            ImageClip(jpg_path)
                .set_duration(every_part_duration_time)  # 图片持续时间
                .set_start(start_time)
        )

        moving_image = clip_image.fl(fl, apply_to=['mask'])

        start_time = start_time + every_part_duration_time
        image_list.append(moving_image.set_pos(set_pos))
    print("图片拼接函数处理完毕！")


    # 处理文字
    start_time = 0  # 再次定义添加文字的起始时间
    str_list = []  # 设置添加文字处理效果后的结果集合

    for num in range(len(strs_list)):
        # 获取该字段字符串
        words = strs_list[num]
        # 每段字幕时长
        every_part_duration_time = mp3_duration / len(strs_list)
        # 字幕数据
        title_clip = (
            TextClip(strs_list[num], font=font_path, fontsize=50, color='white', method='label')
                .set_position(("center", "bottom"))
                .set_duration(every_part_duration_time)
                .set_start(start_time)
        )
        start_time = start_time + every_part_duration_time
        str_list.append(title_clip)
    print("字幕拼接函数处理完毕！")


    # 在视频中添加水印
    logo = (ImageClip(logo_path)
            .set_duration(mp3_duration)  # 水印持续时间
            .resize(height=100)  # 水印的高度，会等比缩放
            # .margin(right=8, top=8, opacity=1) # 水印边距和透明度
            .set_pos(("right", "top")))  # 水印的位置
    print("视频添加水印完毕！")


    # 载入背景视频
    path = "materials_base/base1280_720.mp4"
    video = VideoFileClip(path).resize((1280, 720)).set_duration(mp3_duration)
    cvc = CompositeVideoClip([video] + image_list + str_list + [logo], size=(1280, 720))
    print("在背景视频中处理字幕和拼接图片完毕！")


    # 读取处理过的音频
    mp3_path = "./materials/" + title + "/data/" + title + ".mp3"
    audio_clip = AudioFileClip(mp3_path)
    cvc = cvc.set_audio(audio_clip)
    print("解说音频合成在视频音轨完毕！")

    # 合成定义好的素材，开头、结尾、封面3部分
    L = []  # 定义合成的素材集合
    video = VideoFileClip(cover_mp4).resize((1280, 720))
    L.append(video)
    video = VideoFileClip(strat_mp4).resize((1280, 720))
    L.append(video)
    video = cvc.resize((1280, 720)).fadein(2, (1, 1, 1))
    L.append(video)
    video = VideoFileClip(end_mp4).resize((1280, 720))
    video = video.set_duration(video.duration - 0.5)
    L.append(video)
    final_clip = concatenate_videoclips(L)
    print("视频内容拼接完毕！")

    # 生成目标视频文件
    final_clip.to_videofile('materials/' + title + '/data/' + title + '.mp4', fps=60, remove_temp=False)
    # cvc.write_videofile("./materials/" + title + "/data/result.mp4", fps=60, remove_temp=False, verbose=True)

    print("背景视频中添加轮播图片、字幕、音频解说合成完毕，保存目录：", "./materials/" + title + "/data/")















