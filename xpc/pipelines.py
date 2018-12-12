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
        self.r = redis.Redis(host='www.donogh.cn', port=6379,db=15,password='donogh')

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
            db='xpc_gp1',
            user='donogh',
            password='donogh',
            charset='utf8mb4',
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        # keys = item.keys()
        # values = [item[k] for k in keys]
        keys, values = zip(*item.items())
        sql = "insert into `{}` ({}) values ({}) " \
              "ON DUPLICATE KEY UPDATE {}".format(
            item.table_name,
            ','.join(keys),
            ','.join(['%s'] * len(values)),
            ','.join(['`{}`=%s'.format(k) for k in keys])
        )
        self.cur.execute(sql, values * 2)
        self.conn.commit()
        print(self.cur._last_executed)
        return item
