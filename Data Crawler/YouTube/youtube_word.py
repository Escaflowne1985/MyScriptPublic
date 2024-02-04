# coding=utf-8
import requests
import you_get
import os
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import threading


# 定义一个函数，该函数将在每个线程中运行
def run_cmd(cmd):
    os.system(cmd)


# 获取视频地址
def split_name(text):
    return text.split("v=")[-1]


with open("keywords.txt", encoding="utf8") as f:
    data = f.readlines()
music_name_list = [i.replace("\n", "").split("&") for i in data]
print(music_name_list)

cmd_list = []

for music_name in music_name_list:
    # 创建文件夹
    music_path = "data/" + music_name[0] + "/"
    if not os.path.exists(music_path):
        os.makedirs(music_path)

    cmd = r'yt-dlp -o "data/{}/%(title)s.%(ext)s" -f bestvideo+bestaudio --proxy http://127.0.0.1:19180/ "ytsearch100:{}"'.format(
        music_name[0], music_name[1])
    cmd_list.append(cmd)

# 创建线程列表
threads = []
for cmd in cmd_list:
    # 创建一个新的线程
    t = threading.Thread(target=run_cmd, args=(cmd,))
    # 将线程添加到列表中
    threads.append(t)
    # 启动线程
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()
