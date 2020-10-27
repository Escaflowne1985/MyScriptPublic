#coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '对文字处理的各种方法'

import csv
from aip import AipNlp

# 抓取信息保存的方法
def write_csv(path, data_row):
    with open(path,'a+',encoding="utf-8-sig") as f:
        csv_write = csv.writer(f)
        csv_write.writerow(data_row)

# 对文字字幕进行分行处理
def clean_word(word):
    word_len = int(len(word) / 20)
    word_num = 0
    while word_num <= word_len:
        if word_num == 0:
            strs = word[:(word_num + 1) * 20] + "\n"
        else:
            #             strs = word[:(word_num + 1) * 8] + "..."
            strs = strs + word[word_num * 20:(word_num + 1) * 20] + "\n"
        word_num = word_num + 1
    return word_len, strs


# 文章摘要处理
def make_summary(title,content):
    APP_ID = '你的APP_ID'
    API_KEY = '你的API_KEY'
    SECRET_KEY = '你的SECRET_KEY'
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    if len(content)>300:
        maxSummaryLen = 300
        client.newsSummary(content, maxSummaryLen)
        options = {}
        options["title"] = title
        newsSummary_result = client.newsSummary(content, maxSummaryLen, options)
        return newsSummary_result["summary"]
    else:
        return content