# -*- coding: utf-8 -*-
import scrapy


class NewsDataItem(scrapy.Item):
    title = scrapy.Field()  # 新闻标题
    url = scrapy.Field()  # 原文链接
    publishTime = scrapy.Field()  # 发布时间
    content = scrapy.Field()  # 文章正文
    new_type = scrapy.Field()  # 新闻类别
    web_name = scrapy.Field()  # 网站名称
    channel_name = scrapy.Field()  # 频道名称
