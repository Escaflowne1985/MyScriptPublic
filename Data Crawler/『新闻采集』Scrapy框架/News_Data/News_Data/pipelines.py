# -*- coding: utf-8 -*-
# 添加必备包和加载设置
import pymongo
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class NewsDataPipeline(object):
    # class中全部替换
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DATABASE"]
        sheetname = settings["MONGODB_SHEETNAME"]
        username = settings["MONGODB_USER"]
        password = settings["MONGODB_PASSWORD"]

        print(host, port, dbname, sheetname)
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # client = pymongo.MongoClient(host=host, port=port, username=username, password=password)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert_one(data)
        return item
