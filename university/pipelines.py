# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import redis
from scrapy.exceptions import DropItem


class RedisPipeline(object):
    def open_spider(self, spider):
        self.r = redis.Redis(host='127.0.0.1')

    # def close_spider(self, spider):
    #     self.r.close()

    def process_item(self, item, spider):
        if self.r.sadd(spider.name, item['name']):
            return item
        raise DropItem


class MysqlPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='www.donogh.cn',
            port=3306,
            db='qianmu_gp1',
            user='donogh',
            password='donogh',
            charset='utf8',
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        # keys = item.keys()
        # values = [item[k] for k in keys]
        keys, values = zip(*item.items())
        sql = "insert into `{}` ({}) values ({})".format(
            'universities',
            ','.join(keys),
            ','.join(['%s'] * len(values))
        )
        self.cur.execute(sql, values)
        self.conn.commit()
        print(self.cur._last_executed)
        return item
