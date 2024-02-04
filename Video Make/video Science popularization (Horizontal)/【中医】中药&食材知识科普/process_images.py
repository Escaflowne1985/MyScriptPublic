# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '图片处理程序'

from urllib import parse
import requests
from bs4 import BeautifulSoup
import os, shutil
from removebg import RemoveBg
from PIL import Image
import time


# 百度图片爬虫
def RequestGetImage(pic_name):
    jpg_name = "./material_jpg/" + pic_name + "/" + pic_name + ".jpg"
    if os.path.exists(jpg_name):
        print("该图片的内容已经存在")
    else:
        name_code = parse.quote(pic_name)
        headers = {
            'user-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Referer': 'http://www.zhihu.com/articles'
        }

        # 图片数据采集 中国医药信息查询平台
        name_code = parse.quote(pic_name)
        headers = {
            'user-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Referer': 'http://www.zhihu.com/articles'
        }
        # 获取查询数据列表
        url = "https://www.dayi.org.cn/search?pageNo=1&keyword={}".format(name_code)
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')
        list_url = soup.find_all('a', class_="name")[0]["href"]
        jpg_url = parse.urljoin(url, list_url)
        time.sleep(1)
        html = requests.get(jpg_url, headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')
        jpg_url = soup.find("div", class_="thumb-container").img["src"]
        time.sleep(1)
        html = requests.get(jpg_url)
        with open('material_jpg/' + pic_name + '/' + pic_name + ".jpg", 'wb') as file:
            file.write(html.content)
        file.close()


# 图片抠图
def CutoutJPG(pic_name):
    # 图片抠图处理
    # 33034782@qq.com   ypWN2SE5p57qKMk6jtaaSXRq
    # escaflowne1@126.com   exQr6L4B7Fe5LmnHpw5ZrJ4V
    # escaflowne2@126.com   HhhM9FETxb4NTBqFGbMfWm5d
    rmbg = RemoveBg("ypWN2SE5p57qKMk6jtaaSXRq", "data/error.log")  # 把你的`API Key`填进去
    # 判断视频图片是否存在，若存在则跳过
    png_name = "./material_jpg/" + pic_name + "/" + pic_name + ".jpg_no_bg.png"
    if not os.path.exists(png_name):
        try:
            rmbg.remove_background_from_img_file("./material_jpg/" + pic_name + "/" + pic_name + ".jpg")
        except:  # 如果无法抠图自动处理成png
            shutil.copyfile("./material_jpg/" + pic_name + "/" + pic_name + ".jpg",
                            "./material_jpg/" + pic_name + "/" + pic_name + ".jpg_no_bg.png")
    else:
        print("该图片的内容抠图已经存在")


# 合成封面图片
def CompositeCoverJPG(pic_name):
    # 加载背景图片
    base_img = Image.open('material_jpg/base/base.jpg')
    # 转换图片色到分别表示RGBA的值
    target = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    # 选择png图片显示的区域
    box = (800, 400, 1260, 690)
    # 加载PNG图片
    region = Image.open('material_jpg/' + pic_name + '/' + pic_name + '.jpg_no_bg.png')
    # 确保图片是RGBA格式，大小和box区域一样
    region = region.convert("RGBA")
    region = region.resize((box[2] - box[0], box[3] - box[1]))
    # 将素材图片合成道底板图上
    target.paste(region, box)
    # 将背景图上假如生成号的素材地板透明背景图
    base_img.paste(target, (0, 0), target)  # 第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域，将底图显示出来。
    # base_img.show()
    base_img.save('material_jpg/' + pic_name + '/result.jpg')  # 保存图片
