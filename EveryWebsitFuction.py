#coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '每个网站获取title,content,imglist的方法'

import re
import os
from bs4 import BeautifulSoup
from gerapy_auto_extractor.extractors import extract_detail
import requests

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

    return title,content,imglist

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

    return title,content,imglist