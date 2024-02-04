# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = ''

import os
from moviepy.editor import *
import time
import re
import pandas as pd
import json
import random
import librosa

# 需要确定同步到基础视频，必须有对应歌名的excel表单
music_name = 'TARA_Day by Day'
resize_num = (1920, 1080)

# 数据处理好的表单数据
df = pd.read_excel("syncstart_result/{}.xlsx".format(music_name))
# base_name = random.choice(df["base_file"].tolist())
base_name = "TARA_Day by Day现场版合集 (P1. p1).mp4"

print('本次选取的基础视频是：', base_name)

# 提出异常的数据
df = df[df['start'] < 50]
df = df[df['start'] != 0]


def clip_4():
    # 提取需要的数据
    data = df.sample(3)
    data_list = data.to_dict("records")
    print(data_list)

    resize_num = (1920 / 2, 1080 / 2)

    # 读取base视频
    video_base = VideoFileClip('source_video/{}'.format(base_name))
    video_base = video_base.resize(resize_num)
    # 获取base视频的时长
    video_base_duration = video_base.duration

    # 读取随机生成的3个视频
    video1 = VideoFileClip('source_video/{}'.format(data_list[0]["target_file"]))
    video1_duration = video_base_duration if video1.duration > video_base_duration else video1.duration
    subclip_1 = video1.subclip(0, video1_duration)
    subclip_1 = subclip_1.set_start(data_list[0]["start"])
    subclip_1 = subclip_1.resize(resize_num)

    video2 = VideoFileClip('source_video/{}'.format(data_list[1]["target_file"]))
    video2_duration = video_base_duration if video2.duration > video_base_duration else video2.duration
    subclip_2 = video2.subclip(0, video2_duration)
    subclip_2 = subclip_2.set_start(data_list[1]["start"])
    subclip_2 = subclip_2.resize(resize_num)

    video3 = VideoFileClip('source_video/{}'.format(data_list[2]["target_file"]))
    video3_duration = video_base_duration if video3.duration > video_base_duration else video3.duration
    subclip_3 = video3.subclip(0, video3_duration)
    subclip_3 = subclip_3.set_start(data_list[2]["start"])
    subclip_3 = subclip_3.resize(resize_num)

    final_clip = clips_array([[video_base, subclip_1],
                              [subclip_2, subclip_3]])

    final_clip.write_videofile("result_video/{}_4_mixed.mp4".format(music_name), fps=30)


def clip_6():
    # 提取需要的数据
    data = df.sample(5)
    data_list = data.to_dict("records")
    data_list

    resize_num = (1920 / 3, 1080 / 2)

    # 读取base视频
    video_base = VideoFileClip('source_video/{}'.format(base_name))
    video_base = video_base.resize(resize_num)
    # 获取base视频的时长
    video_base_duration = video_base.duration

    # 读取随机生成的5个视频
    video1 = VideoFileClip('source_video/{}'.format(data_list[0]["target_file"]))
    video1_duration = video_base_duration if video1.duration > video_base_duration else video1.duration
    subclip_1 = video1.subclip(0, video1_duration)
    subclip_1 = subclip_1.set_start(data_list[0]["start"])
    subclip_1 = subclip_1.resize(resize_num)

    video2 = VideoFileClip('source_video/{}'.format(data_list[1]["target_file"]))
    video2_duration = video_base_duration if video2.duration > video_base_duration else video2.duration
    subclip_2 = video2.subclip(0, video2_duration)
    subclip_2 = subclip_2.set_start(data_list[1]["start"])
    subclip_2 = subclip_2.resize(resize_num)

    video3 = VideoFileClip('source_video/{}'.format(data_list[2]["target_file"]))
    video3_duration = video_base_duration if video3.duration > video_base_duration else video3.duration
    subclip_3 = video3.subclip(0, video3_duration)
    subclip_3 = subclip_3.set_start(data_list[2]["start"])
    subclip_3 = subclip_3.resize(resize_num)

    video4 = VideoFileClip('source_video/{}'.format(data_list[3]["target_file"]))
    video4_duration = video_base_duration if video4.duration > video_base_duration else video4.duration
    subclip_4 = video4.subclip(0, video4_duration)
    subclip_4 = subclip_4.set_start(data_list[3]["start"])
    subclip_4 = subclip_4.resize(resize_num)

    video5 = VideoFileClip('source_video/{}'.format(data_list[4]["target_file"]))
    video5_duration = video_base_duration if video5.duration > video_base_duration else video5.duration
    subclip_5 = video5.subclip(0, video5_duration)
    subclip_5 = subclip_5.set_start(data_list[4]["start"])
    subclip_5 = subclip_5.resize(resize_num)

    final_clip = clips_array([[video_base, subclip_1, subclip_2],
                              [subclip_3, subclip_4, subclip_5]])

    final_clip.write_videofile("result_video/{}_6_mixed.mp4".format(music_name), fps=30)


def clip_9():
    # 提取需要的数据
    data = df.sample(6)
    data_list = data.to_dict("records")
    data_list

    resize_num = (1920 / 3, 1080 / 3)

    # 读取base视频
    video_base = VideoFileClip('source_video/{}'.format(base_name))
    video_base = video_base.resize(resize_num)
    # 获取base视频的时长
    video_base_duration = video_base.duration

    # 读取随机生成的5个视频
    video1 = VideoFileClip('source_video/{}'.format(data_list[0]["target_file"]))
    video1_duration = video_base_duration if video1.duration > video_base_duration else video1.duration
    subclip_1 = video1.subclip(0, video1_duration)
    subclip_1 = subclip_1.set_start(data_list[0]["start"])
    subclip_1 = subclip_1.resize(resize_num)

    video2 = VideoFileClip('source_video/{}'.format(data_list[1]["target_file"]))
    video2_duration = video_base_duration if video2.duration > video_base_duration else video2.duration
    subclip_2 = video2.subclip(0, video2_duration)
    subclip_2 = subclip_2.set_start(data_list[1]["start"])
    subclip_2 = subclip_2.resize(resize_num)

    video3 = VideoFileClip('source_video/{}'.format(data_list[2]["target_file"]))
    video3_duration = video_base_duration if video3.duration > video_base_duration else video3.duration
    subclip_3 = video3.subclip(0, video3_duration)
    subclip_3 = subclip_3.set_start(data_list[2]["start"])
    subclip_3 = subclip_3.resize(resize_num)

    video4 = VideoFileClip('source_video/{}'.format(data_list[3]["target_file"]))
    video4_duration = video_base_duration if video4.duration > video_base_duration else video4.duration
    subclip_4 = video4.subclip(0, video4_duration)
    subclip_4 = subclip_4.set_start(data_list[3]["start"])
    subclip_4 = subclip_4.resize(resize_num)

    video5 = VideoFileClip('source_video/{}'.format(data_list[4]["target_file"]))
    video5_duration = video_base_duration if video5.duration > video_base_duration else video5.duration
    subclip_5 = video5.subclip(0, video5_duration)
    subclip_5 = subclip_5.set_start(data_list[4]["start"])
    subclip_5 = subclip_5.resize(resize_num)

    video6 = VideoFileClip('source_video/{}'.format(data_list[5]["target_file"]))
    video6_duration = video_base_duration if video6.duration > video_base_duration else video6.duration
    subclip_6 = video6.subclip(0, video6_duration)
    subclip_6 = subclip_6.set_start(data_list[5]["start"])
    subclip_6 = subclip_6.resize(resize_num)

    video7 = VideoFileClip('source_video/{}'.format(data_list[6]["target_file"]))
    video7_duration = video_base_duration if video7.duration > video_base_duration else video7.duration
    subclip_7 = video7.subclip(0, video7_duration)
    subclip_7 = subclip_7.set_start(data_list[6]["start"])
    subclip_7 = subclip_7.resize(resize_num)

    video8 = VideoFileClip('source_video/{}'.format(data_list[7]["target_file"]))
    video8_duration = video_base_duration if video8.duration > video_base_duration else video8.duration
    subclip_8 = video8.subclip(0, video8_duration)
    subclip_8 = subclip_8.set_start(data_list[7]["start"])
    subclip_8 = subclip_8.resize(resize_num)

    final_clip = clips_array([[video_base, subclip_1, subclip_2],
                              [subclip_3, subclip_4, subclip_5],
                              [subclip_7, subclip_6, subclip_8], ])

    final_clip.write_videofile("result_video/{}_9_mixed.mp4".format(music_name), fps=30)


clip_4()
clip_6()
clip_9()
