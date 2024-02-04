# -*- coding: utf-8 -*-
import scrapy
from News_Data.items import NewsDataItem
import pandas as pd
from .parse_detail import ProcessContent
from urllib import parse
from scrapy.utils.project import get_project_settings
from gerapy_auto_extractor.extractors import *

settings = get_project_settings()


class NewsDataSpider(scrapy.Spider):
    name = 'News_Data'
    allowed_domains = []

    def start_requests(self):
        # 读取数据
        df = pd.read_excel("我的数据抓取列表.xlsx", sheet_name="数据列表")
        # 数据打乱
        df = df.sample(frac=1.0).reset_index(drop=True)
 
        for i in range(len(df)):
            data = df.iloc[i].to_dict()
            print(data)
            # 判断常规网页
            if data['动态加载url'] == '-' and data['url 参数'] == '-':
                yield scrapy.Request(
                    url=data["网址"], meta={'data': data, }, callback=self.parse_static
                )

    def parse_static(self, response):
        data = extract_list(response.text)
        for each in range(len(data)):
            item = NewsDataItem()
            item['title'] = data[each]["title"].strip()
            item['url'] = parse.urljoin(response.url, data[each]["url"])
            item['publishTime'] = ""
            item["new_type"] = response.meta["data"]["类别"]
            item['web_name'] = response.meta["data"]["网站名称"]
            item['channel_name'] = response.meta["data"]["网站频道"]

            print(item)

            yield scrapy.Request(item['url'], callback=self.parse_detail, meta={'item': item})

    # 具体内容在parse_detail.py中
    def parse_detail(self, response):
        item = ProcessContent(self, response)
        yield item
