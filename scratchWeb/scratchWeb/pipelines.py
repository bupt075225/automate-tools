# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class MongoDBPipeline(object):
    def __init__(self, mongo_server, mongo_db, mongo_collection):
        self.mongo_server = mongo_server
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_server=crawler.settings.get("MONGODB_HOST"),
            mongo_db=crawler.settings.get("MONGODB_DATABASE"),
            mongo_collection=crawler.settings.get("MONGODB_COLLECTION")
        )

    def open_spider(self, spider):
        # 建立与MongoDB的连接
        self.client = pymongo.MongoClient(self.mongo_server)
        # 访问数据库对象
        self.db = self.client[self.mongo_db]

    def close_spider(self):
        # 关闭与MongoDB的连接
        self.client.close()

    def process_item(self, item, spider):
        # 向数据库表中插入数据
        self.db[self.mongo_collection].insert(dict(item))
        return item
