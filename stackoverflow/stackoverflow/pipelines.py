# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from scrapy.exceptions import DropItem

class StackoverflowPipeline(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.connection.scrapynew
        self.collection = self.db.stackoverflow

    def process_item(self, item, spider):
        #print(item)
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        if not self.connection or not item:
            return
        self.collection.save(item)

    def __del__(self):
        if self.connection:
            self.connection.close()
