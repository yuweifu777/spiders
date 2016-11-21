# -*- coding: utf-8 -*-
import sys
import datetime

from scrapy.spiders import Spider
from scrapy.http import Request
from news.items import NewsItem

reload(sys)
sys.setdefaultencoding('utf-8')

class CnstockSpider(Spider):
    name = "cnstock"
    allowed_domains = ["cnstock.com"]
    #: hot spot company
    start_urls = [
        "http://company.cnstock.com/company/scp_dsy/tcsy_rdgs/",        # 1.公司新闻
        "http://company.cnstock.com/company/scp_gsxw",                  # 2.公司聚焦
        "http://ggjd.cnstock.com/gglist/search/qmtbbdj/",               # 3.最新解读

    ]

    def parse(self, response):
        sites = response.xpath('//div[@class="main-list"]/ul/li/a/@href').extract()
        for site in sites:
            yield Request(site, callback=self.parse_item)

        words = response.xpath('//div[@class="pagination pagination-centered"]/ul/li/a/text()').extract()
        if words[-2] == u'下一页':
            next_url = response.xpath('//div[@class="pagination pagination-centered"]/ul/li/a/@href').extract()[-2]
            yield Request(next_url, callback=self.parse)

    def parse_item(self, response):
        item = NewsItem()
        item['title'] = response.xpath('//h1[@class="title"]/text()').extract_first()
        item['time'] = response.xpath('//span[@class="timer"]/text()').extract_first()[:10]
        item['time'] = datetime.datetime.strptime(item['time'], '%Y-%m-%d')
        item['content'] = response.xpath('//div[@id="qmt_content_div" and @class="content"]').extract_first()
        if item['content'] is not None:
            item['content'] = item['content']
        item['url'] = response.url
        yield item
