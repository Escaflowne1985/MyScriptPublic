# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = ''

import os
from moviepy.editor import *
from syncstart.syncstart import file_offset
import time
import re
import pandas as pd
import json
import random


# 字符串时、分、秒转换成秒函数
def str2sec(x):
    h, m, s = x.strip().split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


# 字符串时、分、秒、毫秒转换成秒函数
def str2sec_(x):
    if x != "-":
        h, m, s = x.strip().split(':')
        return str(int(h) * 3600 + int(m) * 60 + int(s))
    else:
        return x


# 定义视频文件夹和音频文件夹
source_audio_dir = "source_audio/"
source_video_dir = "source_video/"

# 获取目录下的视频文件
video_list = os.listdir(source_video_dir)

data_list = []

for base in video_list:

    # # 随机选择一个视频作为base视频，其他视频的音轨和其对
    # base = random.choice(video_list)
    # 选择一个时间最长的视频作为基础视频
    # base = "TARA_Day by Day现场版合集 (P2. p2).flv"
    base_video_dir = "source_video/" + base
    # 剔除已经作为base的名称
    # video_list_remove = video_list
    # video_list_remove.remove(base)

    for target in video_list:
        if base == target:
            pass
        else:
            target_video_dir = "source_video/" + target
            data_dict = {
                'in1': """{}""".format(base_video_dir),
                'in2': """{}""".format(target_video_dir),
                'take': 500,
                'show': False,
                # 'show': '-s',
                # 'normalize': True,
                # 'denoise': '-d',
                # 'lowpass': '-l',
                #
                # 'help': '-h',
                # 'version': '--version'
            }

            file, offset = file_offset(**data_dict)
            data_list.append((base, target, offset))
            print(data_dict)

df = pd.DataFrame(data_list, columns=["base_file", "target_file", "start"])
df.to_excel("syncstart_result/" + "T-ara《No.9》" + ".xlsx", index=False)
