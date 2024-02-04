# -*- coding: utf-8 -*-
import scrapy
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
import pymongo
import random
from bs4 import BeautifulSoup
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class CrudedrugSpider(scrapy.Spider):
    name = 'CrudeDrug'
    allowed_domains = []
    start_urls = []

    # 用于循环start_urls中的网址进行遍历抓取，分两种方式
    def start_requests(self):
        n = 500
        while n <= 3000:
            yield scrapy.Request(url='https://db.yaozh.com/zhongyaocai/{}.html'.format(n), meta={'number':n},callback=self.parse)
            n = n + 1

    def parse(self, response):
        print("开始抓取记录数：",response.meta["number"])
        print("----------------")
        # 省市名称
        area_name = [
            "辽宁",
            "吉林",
            "黑龙江",
            "河北",
            "山西",
            "陕西",
            "甘肃",
            "青海",
            "山东",
            "安徽",
            "江苏",
            "浙江",
            "河南",
            "湖北",
            "湖南",
            "江西",
            "台湾",
            "福建",
            "云南",
            "海南",
            "四川",
            "贵州",
            "广东",
            "内蒙古",
            "新疆",
            "广西",
            "西藏",
            "宁夏",
            "北京",
            "上海",
            "天津",
            "重庆",
            "香港",
            "澳门",
        ]

        def clean_area(text):
            area_list = []
            for name in area_name:
                if name in text:
                    area_list.append(name)
            return area_list

        soup = BeautifulSoup(response.text, "lxml")
        l = soup.find("table", class_="table")

        list_ = []
        for i in l.find_all("tr"):
            col_name = i.th.text
            data = (col_name, i.td.span.text.split("\n")[-1].strip())
            list_.append(data)
        df = pd.DataFrame(list_, columns=["col_name", "data"])
        df = df.set_index(["col_name"]).T
        df.reset_index(drop=True, inplace=True)
        # 提取地域信息
        df["省市"] = ""
        df["url"] = response.url
        try:
            df["省市"][0] = clean_area(df["地理分布"][0])
        except:
            df["省市"] = ""

        username = "zgtNewsUser"
        password = "ciiczgtJZFP"
        client = pymongo.MongoClient(host="localhost", port=27017, username=username, password=password)
        db = client['TCM_Datas']
        db.CrudeDrug.insert(df.to_dict('records'))
        # time.sleep(1)
