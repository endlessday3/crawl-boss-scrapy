# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from scrapy_redis.spiders import RedisSpider

from BossZhipin.items import BosszhipinItem


class ZhipinSpider(RedisSpider):
    name = "zhipin"
    redis_key = "zhipin:start_urls"

    # allowed_domains = ["zhipin.com"]
    start_urls = ['https://www.zhipin.com/c101190100/h_101190100/?query=python&page=1&ka=page-1']

    domains = "https://www.zhipin.com/"

    pagenumber = 1
    ka_pagenumber = 1
    url_first = "https://www.zhipin.com/c101190100/h_101190100/?query=python&page="
    url_second = "&ka=page-"

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(ZhipinSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
        while self.pagenumber < 10:
            self.pagenumber += 1
            self.ka_pagenumber += 1
            newurl = self.url_first + str(self.pagenumber) + self.url_second + str(self.ka_pagenumber)
            yield scrapy.Request(url=newurl, callback=self.parse)
            print("@#@#@#@#@#@# new url :" + newurl)

    def parse(self, response):
        print("@@@@@@@@@@@@@@@@@@@@@@@@" + response.url + "@@@@@@@@@@@@@@@@@@@@@@@@@")
        each_selector = response.xpath('//*[@id="main"]/div/div/ul/li')
        item_list = []
        for each in each_selector:
            item = BosszhipinItem()
            # 职位
            item["position"] = each.xpath("./div/div/h3/a/div/text()").extract_first()
            # 工作时间
            item["work_time"] = each.xpath("./div/div/p/text()[2]").extract_first()
            # 学历要求
            item["educational_background"] = each.xpath("./div/div/p/text()[3]").extract_first()
            # 职位url
            item["position_url"] = self.domains + each.xpath("./div/div[1]/h3/a/@href").extract_first()
            # 薪资
            item["salary"] = each.xpath("./div/div/h3/a/span/text()").extract_first()
            # 发布时间
            item["publish_time"] = each.xpath("./div/div[3]/p/text()").extract_first()
            # 公司名
            item["company_name"] = each.xpath("./div/div/div/h3/a/text()").extract_first()
            # 公司成员数
            item["company_members_number"] = each.xpath("./div/div/div/p/text()[3]").extract_first()
            if item["company_members_number"] == "":
                item["company_members_number"] = each.xpath("./div/div/div/p/text()[2]").extract_first()
            # 公司url
            item["company_url"] = self.domains + each.xpath("./div/div[2]/div/h3/a/@href").extract_first()
            item_list.append(item)

        for item in item_list:
            print("$$$$$$$$$$$$item_list长度：", len(item_list))
            position_url = item["position_url"]
            yield scrapy.Request(url=position_url, callback=self.parse_position, meta={"item": item})



    def parse_position(self, response):
        """
        处理职位url的相应页面
        :param response:
        :return:
        """
        item = response.meta["item"]
        company_url = item["company_url"]

        # 职位描述
        item["position_description"] = " ".join(
            response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[3]/div[1]/div/text()')
            .extract()).strip()
        # 职位介绍
        item["position_introduction"] = " ".join(response.xpath('//div[@class="job-sec"][2]/div[@class="text"]/text()')
                                                 .extract())
        # 职位特点
        item["position_facet"] = ",".join(
            response.xpath('//div[@class="job-sec"][2]/div[@class="job-tags"]/span/text()')
            .extract())
        yield scrapy.Request(url=company_url, callback=self.parse_company, meta={"item": item})

    def parse_company(self, response):
        """
        处理公司url的相应页面
        :param response:
        :return:
        """
        item = response.meta["item"]

        # 公司简介
        item["company_introduction"] = " ".join(response.xpath(
            '//div[@class="job-sec"]/div[@class="text fold-text"]/text()')
            .extract())
        item["crawl_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        yield item
