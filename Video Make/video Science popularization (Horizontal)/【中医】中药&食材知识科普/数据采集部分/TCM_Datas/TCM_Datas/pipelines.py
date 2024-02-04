# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# 文件头添加
import pymongo
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class TcmDatasPipeline(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = settings["MONGODB_SHEETNAME"]
        username = settings["MONGODB_USER"]
        password = settings["MONGODB_PASSWORD"]
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port, username=username, password=password)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post = mydb[sheetname]


    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item