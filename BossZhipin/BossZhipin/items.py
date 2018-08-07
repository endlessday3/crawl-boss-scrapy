# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class BosszhipinItem(scrapy.Item):
    # 职位
    position = Field()
    # 工作时间
    work_time = Field()
    # 学历
    educational_background = Field()
    # 职位url
    position_url = Field()
    # 职位描述
    position_description = Field()
    # 职位介绍
    position_introduction = Field()
    # 职位特点
    position_facet = Field()
    # 薪资
    salary = Field()
    # 发布时间
    publish_time = Field()
    # 公司名
    company_name = Field()
    # 公司成员数
    company_members_number = Field()
    # 公司url
    company_url = Field()
    # 公司简介
    company_introduction = Field()
    # 爬取时间
    crawl_time = Field()
    # 爬虫名
    spider_name = Field()
