# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '处理业务的准备工作'

import os
import glob


# 创建素材的各个文件夹
def MakeMaterialDir(pic_name):
    dirs = 'material_everypart/' + pic_name
    if not os.path.exists(dirs):
        os.makedirs(dirs)
        print("创建 " + 'material_everypart/' + pic_name + " 文件夹完毕")

    dirs = 'material_video/' + pic_name
    if not os.path.exists(dirs):
        os.makedirs(dirs)
        print("创建 " + 'material_video/' + pic_name + " 文件夹完毕")

    dirs = 'material_jpg/' + pic_name
    if not os.path.exists(dirs):
        os.makedirs(dirs)
        print("创建 " + 'material_jpg/' + pic_name + " 文件夹完毕")

    dirs = 'material_mp3/' + pic_name
    if not os.path.exists(dirs):
        os.makedirs(dirs)
        print("创建 " + 'material_mp3/' + pic_name + " 文件夹完毕")


# 制作前删除合成语音的文件，否则无法继续
def CleanFiles(pic_name):
    path = "./material_video/" + pic_name
    for infile in glob.glob(os.path.join(path, '*.mp4')):
        os.remove(infile)
    print(pic_name + "material_video 旧文件清理完毕")

    path = "./material_everypart/" + pic_name
    for infile in glob.glob(os.path.join(path, '*.mp4')):
        os.remove(infile)
    print(pic_name + "material_everypart 旧文件清理完毕")

    path = "./material_mp3/" + pic_name
    for infile in glob.glob(os.path.join(path, '*.mp3')):
        os.remove(infile)
    print(pic_name + "material_mp3 旧文件清理完毕")
