# env manage.py/py
# -*- coding: UTF-8 -*-
'''
@Project ：manage.py 
@File    ：自动分割视频.py
@IDE     ：PyCharm 
@Author  ：Mr数据杨
@Date    ：2023/8/9 9:01 
'''

import os
import random

os.makedirs("temp_cut")

cmd = "scenedetect -i demo.mp4  --output temp_cut detect-adaptive split-video"
os.system(cmd)

video_dir = 'temp_cut'
video_list = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith(('.mp4', '.avi', '.mkv', '.mov'))]  # 你可以根据需要添加更多的视频格式
random.shuffle(video_list)  # 随机排序视频文件

# 生成视频文件路径列表文件
with open('video_list.txt', 'w') as f:
    for video in video_list:
        f.write(f"file '{video}'\n")

# 使用ffmpeg拼接视频
os.system("ffmpeg -y -f concat -safe 0 -i video_list.txt -c copy output_concatenated.mp4")

# 替换音频
os.system("ffmpeg -y -i output_concatenated.mp4 -i demo.mp4 -c:v copy -c:a aac -strict experimental -map 0:v -map 1:a -y output_concatenated.mp4")

# 删除临时的视频列表文件
os.remove('video_list.txt')
