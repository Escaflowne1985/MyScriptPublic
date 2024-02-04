# -*- coding: utf-8 -*-
__author__ = 'Mr.数据杨'
__explain__ = '北京旅游网 新闻资讯数据爬虫脚本' \
              'http://www.visitbeijing.com.cn/'

import scrapy
from News_Data.items import NewsDataItem
from .parse_detail import *
from random import shuffle
import json
from urllib import parse


class WwwVisitbeijingComCnSpider(scrapy.Spider):
    name = 'www_visitbeijing_com_cn'
    allowed_domains = []
    web_name = "北京旅游网"
    new_type = "旅游行业信息"

    start_menu = [
        # 购物
        [
            {"channel_name": "购物-购物攻略", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/3lz9bx5k", },
            {"channel_name": "购物-商家信息", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/19iere7b", },
        ],
        # 美食
        [
            {"channel_name": "美食-潮流美食", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/2gmxkd2a", },
            {"channel_name": "美食-地方美食", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/n0bvf6k2", },
            {"channel_name": "美食-老北京美食", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/rlwk9pq8", },
            {"channel_name": "美食-美食资讯", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/18xr1f7c", },
            {"channel_name": "美食-异域美食", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/lhyv22zr", },
        ],
        # 视频
        [
            {"channel_name": "视频-北京故事", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/lYIcryRt", },
            {"channel_name": "视频-京郊游玩", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/8UuPRmMl", },
            {"channel_name": "视频-特色美食", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/Hszvxnoz", },
            {"channel_name": "视频-游记攻略", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/Jx96mrZo", },
            {"channel_name": "视频-展演视频", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/m12rdtUw", },
        ],
        # 文化
        [
            {"channel_name": "文化-创新文化", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/X6ShiQDg", },
            {"channel_name": "文化-古都文化", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/UfLNxEFA", },
            {"channel_name": "文化-红色文化", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/GqJjEBWR", },
            {"channel_name": "文化-京味文化", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/MT7zkjsv", },
            {"channel_name": "文化-特色文化", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/hzuUSDSi", },
            {"channel_name": "文化-演出", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/VsGq9Qv2", },
            {"channel_name": "文化-影视", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/5qMQ0xSf", },
            {"channel_name": "文化-阅读", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/LYZP6P7M", },
            {"channel_name": "文化-展览", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/DXxAEzhZ", },
        ],
        # 游玩
        [
            {"channel_name": "游玩-北京故事", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/8gez50vw", },
            {"channel_name": "游玩-城区游", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/4eek55dr", },
            {"channel_name": "游玩-京郊游", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/enrbw8do", },
            {"channel_name": "游玩-特色主题游-古都文化游", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/judrtkbd", },
            {"channel_name": "游玩-特色主题游-红色旅游", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/l5tf071h", },
            {"channel_name": "游玩-特色主题游-科教游", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/8ubc2gc4", },
            {"channel_name": "游玩-特色主题游-体育游", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/jtquifc7", },
            {"channel_name": "游玩-特色主题游-文创艺术游", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/4g6nqzpv", },
            {"channel_name": "游玩-特色主题游-休闲度假游", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/6th3pk42", },
            {"channel_name": "游玩-特色主题游-长城游", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/fcj713ds", },
            {"channel_name": "游玩-特色主题游-中医养生游", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/5c9yssil", },
            {"channel_name": "游玩-游玩资讯", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/bwzg2a22", },
        ],
        # 住宿
        [
            {"channel_name": "住宿-京郊度假村", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/ce682gi3", },
            {"channel_name": "住宿-酒店", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/ie1974su", },
            {"channel_name": "住宿-民宿", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/njfs2cb7", },
            {"channel_name": "住宿-农家院", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/70rbttge", },
            {"channel_name": "住宿-特色住宿", "url": "http://api-hq1712.visitbeijing.com.cn/article/list/1p2ze2jm", },
        ],
        # 环游号
        [
            {"channel_name": "环游号", "url": "http://mp.visitbeijing.com.cn/api/article/list/recommend", },
            {"channel_name": "环游号-游玩", "url": "http://mp.visitbeijing.com.cn/api/article/list/play", },
            {"channel_name": "环游号-美食", "url": "http://mp.visitbeijing.com.cn/api/article/list/food", },
            {"channel_name": "环游号-住宿", "url": "http://mp.visitbeijing.com.cn/api/article/list/house", },
            {"channel_name": "环游号-购物", "url": "http://mp.visitbeijing.com.cn/api/article/list/shopping", },
            {"channel_name": "环游号-娱展演", "url": "http://mp.visitbeijing.com.cn/api/article/list/ent", },
            {"channel_name": "环游号-行业", "url": "http://mp.visitbeijing.com.cn/api/article/list/industry", },
        ],
        # 旅游图片
        [
            {"channel_name": "旅游图片", "url": "http://s.visitbeijing.com.cn/html/pic-6-1.shtml", },
        ],
    ]

    def start_requests(self):
        parse_list = [
            self.parse1,  # 购物
            self.parse1,  # 美食
            self.parse1,  # 视频
            self.parse1,  # 文化
            self.parse1,  # 游玩
            self.parse1,  # 住宿
            self.parse2,  # 环球号
            self.parse3,  # 旅游图片
        ]

        # 非API接口方法
        start_menu_list = self.start_menu
        shuffle(start_menu_list)  # 打乱每个栏目种的顺序
        for each_menu_num in range(len(start_menu_list)):
            new_list = self.start_menu[each_menu_num]
            shuffle(new_list)  # 打乱每个栏目中的抓取目标
            for each_menu in new_list:
                url = each_menu["url"]
                channel_name = each_menu["channel_name"]
                parse_function = parse_list[each_menu_num]

                yield scrapy.Request(
                    url=url,
                    meta={
                        'url': url,
                        'channel_name': channel_name,
                    },
                    callback=parse_function
                )

    # 抓取内容的配置 parse_list根据定义匹配
    def parse1(self, response):
        html = response.body.decode('utf-8')
        db = json.loads(html)

        for i in db['data']:
            item = NewsDataItem()
            item['title'] = i['title'].strip()
            item['url'] = "http://www.visitbeijing.com.cn/a1/" + i['id']
            item['publishTime'] = ""
            item['channel_name'] = response.meta["channel_name"]
            item['web_name'] = self.web_name
            item["new_type"] = self.new_type
            yield scrapy.Request(item['url'], callback=self.parse_detail, meta={'item': item})

    def parse2(self, response):
        # 抓取选择页面的列表信息，获取的内容均为list，要求长度必须一直否则会出错
        html = response.body.decode('utf-8')
        db = json.loads(html)

        for i in db['data']['articles']:
            item = NewsDataItem()
            item['title'] = i['title'].strip()
            item['url'] = "http://mp.visitbeijing.com.cn/a1/" + i['id']
            item['publishTime'] = ""
            item['channel_name'] = response.meta["channel_name"]
            item['web_name'] = self.web_name
            item["new_type"] = self.new_type
            yield scrapy.Request(item['url'], callback=self.parse_detail, meta={'item': item})

    def parse3(self, response):
        Item_title = response.xpath('//div[@class="tao"]/a/@title').extract()  # 文章标题列表
        Item_url = response.xpath('//div[@class="tao"]/a/@href').extract()  # 文章链接列表

        for each in range(len(Item_title)):
            item = NewsDataItem()
            item['title'] = Item_title[each].strip()
            item['url'] = parse.urljoin(response.url, Item_url[each])
            item['publishTime'] = ""
            item['channel_name'] = response.meta["channel_name"]
            item['web_name'] = self.web_name
            item["new_type"] = self.new_type
            yield scrapy.Request(item['url'], callback=self.parse_detail, meta={'item': item})

    # 具体内容在parse_detail.py中
    def parse_detail(self, response):
        item = ProcessContent(self, response)
        yield item
