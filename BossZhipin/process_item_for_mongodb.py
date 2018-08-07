#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import pymongo
import json

from collections import Iterator, Iterable

import requests


def process_item():
    # 创建redis数据库连接
    rediscli = redis.Redis(host="47.106.77.2", port=6379, db="0")

    # 创建MongoDB数据库连接
    mongocli = pymongo.MongoClient(host="47.106.77.2", port=27017)

    # 创建mongodb数据库名称
    dbname = mongocli["Boss"]
    # 创建mongodb数据库youyuan的表名称
    sheetname = dbname["zhipin"]
    offset = 0

    while offset < 10:
        # redis 数据表名 和 数据
        source, data = rediscli.blpop("zhipin:items")
        offset += 1
        # 将json对象转换为Python对象
        print(source)
        print(data)
        data = json.loads(data)
        # 将数据插入到sheetname表里
        sheetname.insert(data)
        print(offset)


def query():
    # 创建MongoDB数据库连接
    mongocli = pymongo.MongoClient(host="47.106.77.2", port=27017)

    # 创建mongodb数据库名称
    dbname = mongocli["Boss"]
    # 创建mongodb数据库youyuan的表名称
    sheetname = dbname["zhipin"]
    data = sheetname.find_one({"work_time":"1-333年"})
    sheetname.update_one()

    # sheetname.in
    for row in data:
        print(type(row))
    # print(data)


if __name__ == "__main__":
    # process_item()
    # query()
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/67.0.3396.62 Safari/537.36"}
    response = requests.get("https://www.baidu.com/s?ie=utf8&oe=utf8&wd=*args&tn=98010089_dg&ch=3",
                            headers=headers)
    print(response.text)


