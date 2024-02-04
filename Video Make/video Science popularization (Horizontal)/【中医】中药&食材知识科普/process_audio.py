# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '音频处理程序'

from aip import AipSpeech
import os
import librosa

from configs import *  # 工程配置数据

# 加载配置文件
# 提取使用的字体路径 font_path
# 中英文对应的数据列名字典 column_en2cn_dict\column_cn2en_dict
font_path, column_en2cn_dict, column_cn2en_dict = config()


# 读取文字转语音
def ChangeWordsToMp3(dataframe):
    # 把文字转换成语音 将生成的音频文件保存到material_mp3下
    # 加载百度AIP账号
    APP_ID = '25695490'
    API_KEY = 'zbsKNHkCdRoUACOYLjpoaHq0'
    SECRET_KEY = '0FeLEESAvoRuTmHhNgqvP0mEal5ftszV'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 遍历该条df数据每列文字进行语音MP3转换
    for col in dataframe.columns:
        try:
            result = client.synthesis(column_en2cn_dict[col] + dataframe[col][0], 'zh', 1,
                                      {'vol': 12, 'spd': 6, 'per': 5003})
            if not isinstance(result, dict):
                with open('material_mp3/' + dataframe["CnName"][0] + "/" + col + '.mp3', 'wb') as f:
                    f.write(result)
        except:
            pass


# 文字生成MP3的内容属性字典
def Mp3Info(df):
    # 获取MP3的文件列表
    def file_name(file_dir):
        list_ = [files for files in os.walk(file_dir)][0][2]
        filelist = [i for i in list_ if os.path.splitext(i)[1] == '.mp3']
        return filelist

    # 读取文字转语音的MP3 并计算时长
    def get_mp3_duration(audio_path):
        duration = librosa.get_duration(filename=audio_path)
        return duration

    filelist = file_name("./material_mp3/" + df["CnName"][0])

    time_name_dict = {}
    time_num_all = 0  # 总音频的秒数
    for i in filelist:
        time_num = get_mp3_duration("material_mp3/" + df["CnName"][0] + "/" + i)
        time_num_all = time_num_all + time_num
        time_name_dict[i] = time_num

    return time_name_dict
