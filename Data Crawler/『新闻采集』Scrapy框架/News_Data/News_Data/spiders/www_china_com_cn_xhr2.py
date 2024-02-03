# -*- coding: utf-8 -*-
__author__ = 'Mr.数据杨'
__explain__ = '中国网 新闻资讯数据爬虫脚本' \
              'http://www.china.com.cn/'

import scrapy
from News_Data.items import NewsDataItem
from .parse_detail import *
from urllib import parse
import json
from random import shuffle
from gerapy_auto_extractor.extractors import *


class WwwChinaComCnXhr2Spider(scrapy.Spider):
    name = 'www_china_com_cn_xhr2'
    allowed_domains = []
    web_name = "中国网"
    new_type = "综合类信息新闻"

    start_menu = [
        #  创氪
        [
            [{
                'channel_name': '创氪-最新',
                'url': ['http://chuangkr.china.com.cn/column/8?navName=最新',
                        'https://gateway.36kr.com/api/mis/nav/newsflash/flow/3001',
                        [{'partner_id': 'web',
                          'param': {'siteId': 3001,
                                    'platformId': 2,
                                    'navId': '8',
                                    'pageSize': 20,
                                    'pageEvent': 0,
                                    'pageCallback': ''}}]]},
                {
                    'channel_name': '创氪-推荐',
                    'url': ['http://chuangkr.china.com.cn/column/31?navName=推荐',
                            'https://gateway.36kr.com/api/mis/nav/newsflash/flow/3002',
                            [{'partner_id': 'web',
                              'param': {'siteId': 3001,
                                        'platformId': 2,
                                        'navId': '31',
                                        'pageSize': 20,
                                        'pageEvent': 0,
                                        'pageCallback': ''}}]]},
                {
                    'channel_name': '创氪-创投',
                    'url': ['http://chuangkr.china.com.cn/column/25?navName=创投',
                            'https://gateway.36kr.com/api/mis/nav/newsflash/flow/3003',
                            [{'partner_id': 'web',
                              'param': {'siteId': 3001,
                                        'platformId': 2,
                                        'navId': '25',
                                        'pageSize': 20,
                                        'pageEvent': 0,
                                        'pageCallback': ''}}]]},
                {
                    'channel_name': '创氪-汽车',
                    'url': ['http://chuangkr.china.com.cn/column/22?navName=汽车',
                            'https://gateway.36kr.com/api/mis/nav/newsflash/flow/3004',
                            [{'partner_id': 'web',
                              'param': {'siteId': 3001,
                                        'platformId': 2,
                                        'navId': '22',
                                        'pageSize': 20,
                                        'pageEvent': 0,
                                        'pageCallback': ''}}]]},
                {
                    'channel_name': '创氪-科技',
                    'url': ['http://chuangkr.china.com.cn/column/27?navName=科技',
                            'https://gateway.36kr.com/api/mis/nav/newsflash/flow/3005',
                            [{'partner_id': 'web',
                              'param': {'siteId': 3001,
                                        'platformId': 2,
                                        'navId': '27',
                                        'pageSize': 20,
                                        'pageEvent': 0,
                                        'pageCallback': ''}}]]},
                {
                    'channel_name': '创氪-企服',
                    'url': ['http://chuangkr.china.com.cn/column/24?navName=企服',
                            'https://gateway.36kr.com/api/mis/nav/newsflash/flow/3006',
                            [{'partner_id': 'web',
                              'param': {'siteId': 3001,
                                        'platformId': 2,
                                        'navId': '24',
                                        'pageSize': 20,
                                        'pageEvent': 0,
                                        'pageCallback': ''}}]]},
                {
                    'channel_name': '创氪-生活',
                    'url': ['http://chuangkr.china.com.cn/column/26?navName=生活',
                            'https://gateway.36kr.com/api/mis/nav/newsflash/flow/3007',
                            [{'partner_id': 'web',
                              'param': {'siteId': 3001,
                                        'platformId': 2,
                                        'navId': '26',
                                        'pageSize': 20,
                                        'pageEvent': 0,
                                        'pageCallback': ''}}]]},
                {
                    'channel_name': '创氪-职场',
                    'url': ['http://chuangkr.china.com.cn/column/28?navName=职场',
                            'https://gateway.36kr.com/api/mis/nav/newsflash/flow/3008',
                            [{'partner_id': 'web',
                              'param': {'siteId': 3001,
                                        'platformId': 2,
                                        'navId': '28',
                                        'pageSize': 20,
                                        'pageEvent': 0,
                                        'pageCallback': ''}}]]},
                {
                    'channel_name': '创氪-创新',
                    'url': ['http://chuangkr.china.com.cn/column/23?navName=创新',
                            'https://gateway.36kr.com/api/mis/nav/newsflash/flow/3009',
                            [{'partner_id': 'web',
                              'param': {'siteId': 3001,
                                        'platformId': 2,
                                        'navId': '23',
                                        'pageSize': 20,
                                        'pageEvent': 0,
                                        'pageCallback': ''}}]]},
                {
                    'channel_name': '创氪-房产',
                    'url': ['http://chuangkr.china.com.cn/column/29?navName=房产',
                            'https://gateway.36kr.com/api/mis/nav/newsflash/flow/3010',
                            [{'partner_id': 'web',
                              'param': {'siteId': 3001,
                                        'platformId': 2,
                                        'navId': '29',
                                        'pageSize': 20,
                                        'pageEvent': 0,
                                        'pageCallback': ''}}]]},
                {
                    'channel_name': '创氪-快讯',
                    'url': ['http://chuangkr.china.com.cn/column/newsflash?navName=快讯',
                            'https://gateway.36kr.com/api/mis/nav/newsflash/flow/3001',
                            [{'partner_id': 'web',
                              'param': {'siteId': 3001,
                                        'platformId': 2,
                                        'pageSize': 20,
                                        'pageEvent': 0,
                                        'pageCallback': ''}}]]}]
        ],
    ]

    def start_requests(self):
        parse_list = [
            self.parse1,
        ]

        # 非API接口方法
        start_menu_list = self.start_menu
        shuffle(start_menu_list)  # 打乱每个栏目种的顺序
        for each_menu_num in range(len(start_menu_list)):
            new_list = self.start_menu[each_menu_num]
            shuffle(new_list)  # 打乱每个栏目中的抓取目标
            for each_menu in new_list[0]:
                url = each_menu["url"][1]
                channel_name = each_menu["channel_name"]
                parse_function = parse_list[each_menu_num]
                yield scrapy.FormRequest(url=url,
                                         method='POST',
                                         headers={'Content-Type': 'application/json'},
                                         meta={'channel_name': channel_name},
                                         body=json.dumps((each_menu["url"][2][0])),
                                         callback=parse_function)

    # 抓取内容的配置 parse_list根据定义匹配
    def parse1(self, response):
        html = response.body.decode('utf-8')
        db = json.loads(html)
        for each in db['data']["itemList"]:
            item = NewsDataItem()  # 这里对应Item里的类名
            item['title'] = each["templateMaterial"]["widgetTitle"].strip()  # 新闻标题
            item['url'] = parse.urljoin("http://chuangkr.china.com.cn/p/", str(each["itemId"]))
            item['publishTime'] = ""
            item['channel_name'] = response.meta["channel_name"]
            item['web_name'] = self.web_name
            item["new_type"] = self.new_type

            yield scrapy.Request(item['url'], callback=self.parse_detail, meta={'item': item})

    # 具体内容在parse_detail.py中
    def parse_detail(self, response):
        item = ProcessContent(self, response)
        yield item
