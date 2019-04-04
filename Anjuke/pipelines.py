# -*- coding: utf-8 -*-
import pymysql
from pymysql import cursors
from twisted.enterprise import adbapi


class AnjukePipeline(object):

    def open_spider(self, spider):
        MySQL_INFO = spider.settings['MYSQL']
        self.db = pymysql.connect(**MySQL_INFO)
        self.cursor = self.db.cursor()


    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()


    def process_item(self, item, spider):
        keys, values = dict(item).keys(), dict(item).values()
        try:
            self.cursor.execute("INSERT INTO anjuke_zf({}) VALUES ({});".format(",".join(keys), "'" + "','".join(values) + "'"))
            self.db.commit()
            return item
        except Exception as e:
            self.db.rollback()
        

# 异步处理入库
class AnjukeTwistedPipeline(object):

    def __init__(self):
        MySQL = {
                'host': '127.0.0.1',
                'port': 3306,
                'user': 'root',
                'passwd': '1234',
                'db': 'anjuke',
                'charset': 'utf8',
                'cursorclass': cursors.DictCursor
            }
        self.dbpool = adbapi.ConnectionPool('pymysql', **MySQL)
    

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error,item, spider)


    def insert_item(self, cursor, item):
        keys, values = dict(item).keys(), dict(item).values()
        cursor.execute("INSERT INTO anjuke_zf({}) VALUES ({});".format(",".join(keys), "'" + "','".join(values) + "'"))


    def handle_error(self, error, item, spider):
        print('='*20 + 'error' + '='*20)
        print(error)
        print('='*20 + 'error' + '='*20)