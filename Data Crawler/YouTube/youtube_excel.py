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


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
}
proxies = {'http': 'http://127.0.0.1:1080', 'https': 'http://127.0.0.1:1080'}

df = pd.read_excel("youtube.xlsx")
# 输入要批量下载的歌曲名称
music_name = "Day By Day"
music_name_list = df["歌曲名称"].unique()

for music_name in music_name_list:

    # 判断歌曲文件夹是否存在
    music_path = "data/" + music_name + "/"
    if not os.path.exists(music_path):
        os.makedirs(music_path)

        # 提取对应的数据
        df_temp = df[df["歌曲名称"] == music_name]
        df_temp.reset_index(drop=True, inplace=True)
        df_temp["address"] = df_temp["视频地址"].apply(split_name)

        cmd_list = []
        for i in range(len(df_temp)):
        # for i in range(1):
            url = df_temp["视频地址"][i]
            # # 访问链接
            # html = requests.get(url, headers=headers, proxies=proxies).text
            # # print(html)
            #
            # try:
            #     # 解析提取分辨率列表,提取可选分辨率的 匹配 "adaptiveFormats":[xxxx]
            #     pattern = r'"adaptiveFormats":\[(.*?)\]'
            #     # 提取匹配的内容
            #     match = re.search(pattern, html)
            #     adaptive_formats = match.group(1)
            #
            #     # 匹配 "itag":数字 的正则表达式
            #     pattern = r'"itag":(\d+)'
            #     # 使用 re.findall() 函数提取所有符合模式的数据
            #     matches = re.findall(pattern, adaptive_formats)
            #     # 提取最高分辨率的tag
            #     # tag = matches[0]
            #     # print(tag)
            #
            #     # cmd = r"you-get -o ./downloads --cookies=C:\Users\pc\AppData\Roaming\Mozilla\Firefox\Profiles\1m36u5iu.default-release\cookies.sqlite -x http://127.0.0.1:19180 --itag={} {} --debug".format(tag, url)
            #     cmd = r"you-get -o {} -x http://127.0.0.1:1080  --itag={} {} --debug".format(music_path, matches[0],url)
            #     print(cmd)
            # except:
            #     cmd = r"you-get -o {} -x http://127.0.0.1:1080  {} --debug".format(music_path, url)
            #     print(cmd)

            cmd = r"yt-dlp -o {}/%(title)s.%(ext)s -f bestvideo+bestaudio --proxy http://127.0.0.1:1080/ {}".format(music_path,url)
            print(cmd)
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
