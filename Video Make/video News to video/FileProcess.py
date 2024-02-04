# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '素材文件内容操作'

import os
import glob

# 删除无用的文件
def DeleteFiles():
    # 删除生成的mp3文件
    path = './'
    for infile in glob.glob(os.path.join(path, '*.mp3')):
        os.remove(infile)