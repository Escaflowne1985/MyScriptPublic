# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '每个网站获取title,content,imglist的方法'

import re
import os
from bs4 import BeautifulSoup
from gerapy_auto_extractor.extractors import extract_detail
import requests
import random

# 浏览器header
USER_AGENT_LIST = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

# 随机选择一个header
headers = {
    "User-Agent": random.choice(USER_AGENT_LIST),
}

# vpn代理
proxies = {
    "http": "http://127.0.0.1:19180",
    "https": "https://127.0.0.1:19180"
}


def www_177521_com(response):
    title = extract_detail(response.text)["title"]
    title = title.strip()  # 去除正文中的格式
    title = re.sub(r'[\u3000]', '', title)  # 正则替换掉无用的内容
    # 获取网页中内容正文
    soup = BeautifulSoup(response.text, "lxml")  # 解析网页
    content_text = soup.find("div", class_="image_div")  # 提取正文内容
    content = content_text.text.strip()  # 去除正文中的格式
    content = re.sub(r'[\r\n\xa0 ]', '', content)  # 正则替换掉无用的内容
    # 获取网页中的图片信息
    reg = r'src="(.+?\.jpg)"'
    imgre = re.compile(reg)
    imglist = imgre.findall(str(content_text))
    try:
        page_info = BeautifulSoup(response.text, "lxml")
        link_list = []
        for i in page_info.find_all("a", class_="page-numbers"):
            link_list.append("https://www.177521.com" + i["href"])
        link_list = list(set(link_list))
        # 遍历后面的页面抓取图片
        for link_url in link_list:
            response = requests.get(link_url)
            soup = BeautifulSoup(response.text, "lxml")  # 解析网页
            content_text = soup.find("div", class_="image_div")  # 提取正文内容
            # 获取网页中的图片信息
            reg = r'src="(.+?\.jpg)"'
            imgre = re.compile(reg)
            link_jpgs = imgre.findall(str(content_text))
            imglist = imglist + link_jpgs
    except:
        print("该内容只有一页")

    return title, content, imglist


def www_sohu_com(response):
    title = extract_detail(response.text)["title"]
    title = title.strip()  # 去除正文中的格式
    title = re.sub(r'[\u3000]', '', title)  # 正则替换掉无用的内容
    # 获取网页中内容正文
    soup = BeautifulSoup(response.text, "lxml")  # 解析网页
    content_text = soup.find("article", class_="article")  # 提取正文内容
    content = content_text.text.strip()  # 去除正文中的格式
    content = re.sub(r'[\r\n\xa0 ]', '', content)  # 正则替换掉无用的内容
    # 获取网页中的图片信息
    reg = r'src="(.+?\.jpeg)"'
    imgre = re.compile(reg)
    imglist = imgre.findall(str(content_text))
    return title, content, imglist


# haopinang.com
def haopinang(response):
    response.encoding = 'utf8'
    title = extract_detail(response.text)["title"]
    title = title.strip()  # 去除正文中的格式
    title = re.sub(r'[\u3000]', '', title)  # 正则替换掉无用的内容
    # 获取网页中内容正文
    soup = BeautifulSoup(response.text, "lxml")  # 解析网页
    content_text = soup.find("article", class_="article-content")  # 提取正文内容
    content = content_text.text.strip()  # 去除正文中的格式
    content = re.sub(r'[\r\n\xa0]', '', content)  # 正则替换掉无用的内容
    # 替换掉文章中通用的标准格式字符
    content.replace("好皮囊：将来或许容颜会消逝，但照片的你永远不会老去", "")

    # 获取网页中的图片信息
    imglist = ["https:" + i for i in re.findall('src="(.*?)"', str(content_text), re.S) if "jpg" in i]
    imglist = set(imglist)
    imglist = [i for i in imglist]
    return title, content, imglist
