# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
import pymysql
import json
import sqlite3
from sqlite3 import OperationalError

class WechatThepublicPipeline(object):
    def __init__(self):
        # 连接MySQL数据库
        # self.connect = pymysql.connect(
        #     host='127.0.0.1',  # 数据库地址
        #     port=3306,  # 数据库端口
        #     db='WeChat_ThePublic',  # 数据库名
        #     user='root',  # 数据库用户名
        #     passwd='admin',  # 数据库密码
        #     charset='utf8',  # 编码方式
        #     use_unicode=True)
        #
        # # 通过cursor执行增删查改
        # self.cursor = self.connect.cursor()

        #连接SQLite
        self.connect = sqlite3.connect('./data/WeChat_ThePublic.db')
        print("Opened database successfully")
        self.cursor = self.connect.cursor()
        try:
            self.cursor.execute('''CREATE TABLE file_articles
                                   (ID INT PRIMARY KEY  ,             
                                    title varchar(300) not null,
                                    url varchar(100),
                                    keywords varchar(100),
                                    author varchar(500),
                                    published_time varchar(50),
                                    picture_url_list varchar(500),
                                    content mediumtext);''')
            self.connect.commit()
        except OperationalError:
            print("table domestic already exists")

    def open_spider(self, spider):
        self.fp = open("./data/news_data.json", "wb")
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding="utf-8")

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        self.cursor.execute(
            """insert into file_articles (title, url, keywords ,author, published_time, picture_url_list, content) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"""
            % (item['title'],  # item里面定义的字段和表字段对应
             item['url'],
             item['keywords'],
             item['author'],
             item['published_time'],
             json.dumps(item['picture_url_list']),
             item['content']))

        # 提交sql语句
        self.connect.commit()
        return item

    def close_spider(self, spider):
        self.fp.close()
        self.connect.close()
        pass