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
music_name = 'T-ara《No.9》'
resize_num = (1920, 1080)

# 数据处理好的表单数据
df = pd.read_excel("syncstart_result/{}.xlsx".format(music_name), sheet_name="Sheet1")
base_name = random.choice(df["base_file"].tolist())
# base_name = "티아라_넘버나인 (Number 9 by T-ara@Mcountdown 2013.10.31).mp4"

print('本次选取的基础视频是：', base_name)

# 提出异常的数据
df = df[df['start'] < 50]
df = df[df['start'] != 0]


def clip_mix():
    # 读取base视频
    video_base = VideoFileClip('video_source/{}'.format(base_name))
    video_base = video_base.resize(resize_num)
    # 获取base视频的时长
    video_base_duration = video_base.duration
    # 设置视频最大时间
    stop_time = video_base_duration

    # 循环创建变量、裁剪、重置分辨率
    num_list = list(range(len(df)))
    video_list = df.to_dict('records')

    # 读取base视频
    video_base = VideoFileClip('video_source/{}'.format(base_name))
    video_base = video_base.resize(resize_num)
    # 获取base视频的时长
    video_base_duration = video_base.duration

    # # 随机生成每次切割的时间点
    # time_ = 0
    # start_time = 0

    # time_list = [0]
    # # 判断时间永远小于要做的视频
    # while time_ <= stop_time:
    #     # 视频随机切割点
    #     # 设置一个随机秒数的因子变量
    #     cut_time = random.randint(5, 10)
    #     start_time = start_time + cut_time
    #     time_list.append(start_time)
    #     # 最终计算变量
    #     time_ = time_ + cut_time
    #
    # # 剔除超出的部分时间,多处理一个防止放生意外
    # time_list = time_list[:-2]
    #
    # # 时间两两组合成需要拆的部分视频
    # time_list = [time_list[i:i + 2] for i in range(0, len(time_list), 1)]
    #
    # # 为最后一个元素添加 结束时间 stop_time
    # time_list[-1] = [time_list[-1][0], stop_time]
    # # 生成需要开始替换的视频片段时间列表
    # time_list_cut = time_list[1:-1]

    # 读取base视频
    video_base = VideoFileClip('video_source/{}'.format(base_name))
    video_base = video_base.resize(resize_num)
    # 获取base视频的时长
    video_base_duration = video_base.duration
    # 设置视频最大时间
    stop_time = video_base_duration

    # 循环创建变量、裁剪、重置分辨率
    num_list = list(range(len(df)))
    video_dict = df[df["base_file"] == base_name].to_dict('records')
    video_dict.append({'file_name': '{}'.format(base_name), 'start': 0})
    # 构建变量名称，调用使用 locals()[xxxx]方法
    video_list = []
    end_list = []
    for num, data in zip(num_list, video_dict):
        if data.get("target_file"):
            print(data["target_file"], '同步视频已加入队列')
            locals()["video_temp_" + str(num)] = VideoFileClip("video_source/" + data["target_file"])
        else:
            print(data["file_name"], 'base 视频视频已加入队列')
            locals()["video_temp_" + str(num)] = VideoFileClip("video_source/" + data["file_name"])
        # 统一分辨率
        locals()["video_temp_" + str(num)] = locals()["video_temp_" + str(num)].resize(resize_num)
        # 计算每个视频的最大时间
        end_time = video_base_duration if locals()["video_temp_" + str(num)].duration > video_base_duration else \
            locals()["video_temp_" + str(num)].duration
        #     print(end_time)
        # 对视频的结束时间进行计算统一≤base视频时间
        locals()["video_temp_" + str(num)] = locals()["video_temp_" + str(num)].subclip(0, end_time)
        # 设置每个同步视频的开始时间
        #     locals()["video_temp_"+str(num)] = locals()["video_temp_"+str(num)].set_start(video_dict[num]["start"])
        #        # 视频按照裁剪时间重新定义变量
        #     locals()["video_temp_"+str(num)] = locals()["video_temp_"+str(num)].subclip(start_time,end_time)
        video_list.append((video_dict[num], "video_temp_" + str(num)))
        end_list.append(locals()["video_temp_" + str(num)].duration)

    # 读取音频文件
    # audio = AudioFileClip("wav_plot/high.wav")
    # 获取音乐节拍
    x, sr = librosa.load('video_source/{}'.format(base_name))
    # 构建节拍fram
    onset_frames = librosa.onset.onset_detect(x, sr=sr)
    # 转换音乐节拍切换成秒数
    onset_times = librosa.frames_to_time(onset_frames)
    # 将秒数时间保留两位小暑
    onset_times = [round(i, 2) for i in onset_times]
    # 防止音乐节奏太快降低转换频率
    for n in range(30):
        try:
            for i in range(len(onset_times)):
                if onset_times[i + 1] - onset_times[i] <= 1:
                    onset_times.remove(onset_times[i])
        except:
            pass
    # 取切换素材第一个点为起始点
    start_time = min(df["start"]) + 1
    # 去切换素材结束的时间最小为终点
    end_time = min(end_list)
    # 提取 onset_times 范围内的节点作为切换节点
    onset_times_ = [x for x in onset_times if start_time < x < end_time]
    # 列表数据首位追加整个视频的开始和终点
    onset_times_.append(video_base_duration)
    onset_times_.append(0)
    onset_times_.sort()
    # 时间两两组合成需要拆的部分视频
    time_list = [onset_times_[i:i + 2] for i in range(0, len(onset_times_), 1)]
    # 剔除无用末尾元素
    if time_list[-1][0] == time_list[-2][1]:
        time_list.pop()

    # 删除无素材的末尾元素以防出错
    for i in time_list:
        if i[1] >= end_time:
            time_list.pop()
    time_list_cut = time_list

    L = []
    n = 1

    for time_ in time_list_cut:
        #     print(time_)
        temp_ = random.choice(video_list)  # ({'file_name': '7.mp4', 'start': 9.199909297052153}, 'video_temp_4')
        video = locals()[temp_[1]].set_start(temp_[0][
                                                 "start"])  # .subclip(time_[0]+temp_[0]["start"],time_[1]+temp_[0]["start"]) # <moviepy.video.io.VideoFileClip.VideoFileClip at 0x210b5d97df0>
        video = video.subclip(time_[0], time_[1])

        video = video.resize(resize_num)
        video_clip = (
            video
                .set_start(time_[0] + temp_[0]["start"])
                .set_duration((time_[1] - time_[0]))
                .set_position(("center", "center"))
        )
        locals()["video_clip" + str(n)] = video_clip
        L.append(locals()["video_clip" + str(n)])
        n = n + 1

    cvc = CompositeVideoClip([video_base] + L)
    cvc = cvc.set_audio(None)
    cvc = cvc.set_audio(video_base.audio)
    cvc.write_videofile("video_result/{}_music_point_mixed.mp4".format(music_name), fps=30)


clip_mix()
