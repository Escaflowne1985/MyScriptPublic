# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '处理音频内容的方法'

from aip import AipSpeech
import os

"""读取文字转语音 加载百度AIP账号"""
APP_ID = '25695490'
API_KEY = 'zbsKNHkCdRoUACOYLjpoaHq0'
SECRET_KEY = '0FeLEESAvoRuTmHhNgqvP0mEal5ftszV'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def StrToMp3(title, content):
    # 判断如果没有该数据的文件夹就创建
    dirs = 'materials/' + title + "/data/"
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    # 根据title、content生成语音
    result = client.synthesis(title + content, 'zh', 1, {'vol': 15, 'spd': 6, 'per': 5118})
    if not isinstance(result, dict):
        with open('materials/' + title + "/data/" + title + '.mp3', 'wb') as f:
            f.write(result)
    print("mp3文件已经生成完毕，在目录：", 'materials/' + title + "/data/")
