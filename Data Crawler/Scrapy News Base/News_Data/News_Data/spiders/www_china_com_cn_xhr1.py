# -*- coding: utf-8 -*-
__author__ = 'Mr.数据杨'
__explain__ = '中国网 新闻资讯数据爬虫脚本' \
              'http://www.china.com.cn/'

import scrapy
from News_Data.items import NewsDataItem
from .parse_detail import *
from urllib import parse
from random import shuffle
import json
from gerapy_auto_extractor.extractors import *


class WwwChinaComCnXhr1Spider(scrapy.Spider):
    name = 'www_china_com_cn_xhr1'
    allowed_domains = []
    web_name = "中国网"
    new_type = "综合类信息新闻"

    start_menu = [
        # 数字演绎服务平台
        [{
            'channel_name': '中国网-数字演绎服务平台-首页',
            'url': ['http://shineup.china.com.cn/Project?channelId=5e6bbda4855d761bcf02d287',
                    'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5e6bbda4855d761bcf02d287&page=1']},
            {
                'channel_name': '中国网-数字演绎服务平台-中华戏曲',
                'url': ['http://shineup.china.com.cn/Project?channelId=5e7af192a6b7a26f2650ae37',
                        'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5e7af192a6b7a26f2650ae37&page=1']},
            {
                'channel_name': '中国网-数字演绎服务平台-原创戏剧',
                'url': ['http://shineup.china.com.cn/Project?channelId=5e7af651a6b7a26f2650ae44',
                        'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5e7af651a6b7a26f2650ae44&page=1']},
            {
                'channel_name': '中国网-数字演绎服务平台-曲艺杂谈',
                'url': ['http://shineup.china.com.cn/Project?channelId=5e7afe35a6b7a26f2650ae59',
                        'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5e7afe35a6b7a26f2650ae59&page=1']},
            {
                'channel_name': '中国网-数字演绎服务平台-音乐剧',
                'url': ['http://shineup.china.com.cn/Project?channelId=5e7affbba6b7a26f2650ae63',
                        'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5e7affbba6b7a26f2650ae63&page=1']},
            {
                'channel_name': '中国网-数字演绎服务平台-新媒体培训',
                'url': ['http://shineup.china.com.cn/Project?channelId=5e808f709d98aa37645ae4ef',
                        'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5e808f709d98aa37645ae4ef&page=1']},
            {
                'channel_name': '中国网-数字演绎服务平台-老年文化',
                'url': ['http://shineup.china.com.cn/Project?channelId=5f55d1953bd46b6a7bccae5d',
                        'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5f55d1953bd46b6a7bccae5d&page=1']},
            {
                'channel_name': '中国网-数字演绎服务平台-助力脱贫攻坚',
                'url': ['http://shineup.china.com.cn/Project?channelId=5fd6c7cee71ffd66d3ecfaa5',
                        'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5fd6c7cee71ffd66d3ecfaa5&page=1']},
            {
                'channel_name': '中国网-数字演绎服务平台-天津京剧院',
                'url': ['http://shineup.china.com.cn/Project?channelId=5e81561fab7ad6563530f027',
                        'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5e81561fab7ad6563530f027&page=1']},
            {
                'channel_name': '中国网-数字演绎服务平台-河南豫剧团',
                'url': ['http://shineup.china.com.cn/Project?channelId=5e8158b6ab7ad6563530f028',
                        'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5e8158b6ab7ad6563530f028&page=1']},
            {
                'channel_name': '中国网-数字演绎服务平台-陕西人艺',
                'url': ['http://shineup.china.com.cn/Project?channelId=5e857cd2ab7ad6563530f055',
                        'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5e857cd2ab7ad6563530f055&page=1']},
            {
                'channel_name': '中国网-数字演绎服务平台-浙江越剧团',
                'url': ['http://shineup.china.com.cn/Project?channelId=5e857d0eab7ad6563530f057',
                        'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5e857d0eab7ad6563530f057&page=1']},
            {
                'channel_name': '中国网-数字演绎服务平台-国家京剧院',
                'url': ['http://shineup.china.com.cn/Project?channelId=5eca1cd1ddcfa213d79cbead',
                        'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5eca1cd1ddcfa213d79cbead&page=1']},
            {
                'channel_name': '中国网-数字演绎服务平台-爱乐传习',
                'url': ['http://shineup.china.com.cn/Project?channelId=5ed8aa14ddcfa213d79cbefe',
                        'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5ed8aa14ddcfa213d79cbefe&page=1']},
            {
                'channel_name': '中国网-数字演绎服务平台-乐器营口大赛',
                'url': ['http://shineup.china.com.cn/Project?channelId=5ed9faa0ddcfa213d79cbf10',
                        'http://shineup.china.com.cn/api/web/article/getListByPage?channelId=5ed9faa0ddcfa213d79cbf10&page=1']}]
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
            for each_menu in new_list:
                url = each_menu["url"][1]
                channel_name = each_menu["channel_name"]
                parse_function = parse_list[each_menu_num]

                yield scrapy.Request(
                    url=url,
                    meta={
                        'channel_name': channel_name,
                    },
                    callback=parse_function
                )

    # 抓取内容的配置 parse_list根据定义匹配
    def parse1(self, response):
        html = response.body.decode('utf-8')
        db = json.loads(html)
        for each in db['data']["list"]:
            item = NewsDataItem()  # 这里对应Item里的类名
            item['title'] = each["articleTitle"].strip()  # 新闻标题
            item['url'] = "http://shineup.china.com.cn/api/web/article/getInfo?articleId=" + str(each["articleId"])
            item['publishTime'] = ""
            item['channel_name'] = response.meta["channel_name"]
            item['web_name'] = self.web_name
            item["new_type"] = self.new_type

            yield scrapy.Request(item['url'], callback=self.parse_detail, meta={'item': item})

    # 具体内容在parse_detail.py中
    def parse_detail(self, response):
        item = response.meta['item']
        html = response.text
        db = json.loads(html)
        item["content"] = db["data"]["leftData"]["content"]
        yield item
