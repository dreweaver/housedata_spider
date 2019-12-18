# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json
from twisted.enterprise import adbapi
from pymysql import cursors
import csv
import os
#class CrawlLianjiaSinglePipeline(object):
    # def __init__(self):
    #     dbparams = dict(
    #         host= 'localhost',
    #         port=3306,
    #         user='root',
    #         password='123456',
    #         database='lianjia',
    #         charset='utf8',
    #         cursorclass=pymysql.cursors.DictCursor, 
    #         use_unicode=True,           
    #     )
    #     self.dbpool = adbapi.ConnectionPool("pymysql", **dbparams)    # 使用twisted将mysql插入变成异步执行

    # def process_item(self, item, spider):
    #     query = self.dbpool.runInteraction(self.do_insert, item)
    #     query.addErrback(self.handle_error, item, spider) #处理异常
    # def do_insert(self,cursor,item):
    #     try:
    #         sql="insert into traderecord(houseinfo1,houseinfo2,dealdate,totalprice,floor,unitprice) values(%s,%s,%s,%s,%s,%d)"
    #         values=(hosueinfo1,houseinfo2,dealdate,totalprice,floor,unitprice)
    #         cursor.execute(sql,values)
    #         print('------fengexian-----')
    #         return item        
    #     except Exception as err:            
    #         pass
    # def handle_error(self,failure,item,spider):
    #     print(failure)
    # def open_spider(self, spider):
    #     self.connect = pymysql.connect(
    #         host='localhost',
    #         user='root',
    #         port=3306,
    #         passwd='123456',
    #         db='lianjia',
    #         charset='utf8'
    #     )
    #     self.cursor = self.connect.cursor()
 
    #def process_item(self, item, spider):
    #     print('哈哈')
    #     print('哈哈')
    #     insert_sql = "INSERT INTO traderecord(houseinfo1,houseinfo2,dealdate,totalprice,floor,unitprice) VALUES (%s, %s, %s, %s, %d, %s, %d)"%(houseinfo1,houseinfo2,dealdate,totalprice,floor,unitprice)
    #     #self.cursor.execute(insert_sql, (item['houseinfo1'],item['houseinfo2'],item['dealdate'],item['totalprice'],item['floor'],item['unitprice']))
    #     self.cursor.execute(insert_sql)
    #     self.connect.commit()
    #    return item
    # def close_spider(self, spider):
    #     self.cursor.close()
    #     self.connect.close()
class CrawlLianjiaSinglePipeline(object):

    def open_spider(self, spider):
        self.file = open('quchongshuju.jl', 'w', encoding='utf8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    # def __init__(self):
    #     # csv文件的位置,无需事先创建
    #     self.store_file = os.path.dirname(__file__) + 'articles.csv'
    #     print("***************************************************************")
    #     # 打开(创建)文件

    #     self.file = open(self.store_file, 'a+', encoding="utf8",newline='')
    #     # csv写法
    #     self.writer = csv.writer(self.file, dialect="excel")

    # def process_item(self, item, spider):
    #     # 判断字段值不为空再写入文件
    #     print("正在写入......")
    #     if item['houseinfo1']:
    #         # 主要是解决存入csv文件时出现的每一个字以‘，’隔离
    #         self.writer.writerow([item['houseinfo1'],item['houseinfo2'],item['dealdate'],item['totalprice'],item['floor'],item['unitprice']])
    #     return item

    # def close_spider(self, spider):
    #     # 关闭爬虫时顺便将文件保存退出
    #     self.file.close()
# class MongoPipeline(object):

#     collection_name = 'scrapy_items'

#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db

#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'lianjia')
#         )

#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]

#     def close_spider(self, spider):
#         self.client.close()

#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert_one(dict(item))
#         return item