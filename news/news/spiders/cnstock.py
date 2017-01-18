# -*- coding: utf-8 -*-
"""
    News from www.cnstock.com.cn (Shanghai Stock Newspaper)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Different section updates with different speed.
    Evaluate the appropriate X page number.
    for i in range(1, X):
        ...
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    2017.1
"""
import sys
import datetime

from scrapy.spiders import Spider
from scrapy.http import Request
from news.items import NewsItem

reload(sys)
sys.setdefaultencoding('utf-8')

class CnstockSpider(Spider):
    """
        downloading urls
        ~~~~~~~~~~~~~~~~
        http://company.cnstock.com/company/scp_dsy/tcsy_rdgs/10
    """
    name = "cnstock"
    allowed_domains = ["cnstock.com"]
    #: hot spot company
    start_urls = [
        "http://company.cnstock.com/company/scp_dsy/tcsy_rdgs/",        # 1.公司新闻
        "http://company.cnstock.com/company/scp_gsxw",                  # 2.公司聚焦
        "http://ggjd.cnstock.com/gglist/search/qmtbbdj/",               # 3.最新解读
    ]

    def start_requests(self):

        # 1. company news
        url = "http://company.cnstock.com/company/scp_dsy/tcsy_rdgs/%s"
        for i in xrange(1, 11):
            download_url = url % i
            yield Request(download_url, self.parse)

        # 2. company focus
        url = "http://company.cnstock.com/company/scp_gsxw/%s"
        for i in xrange(1, 25):
            download_url = url % i
            yield Request(download_url, self.parse)

        # 3. newest analysis
        url = "http://ggjd.cnstock.com/gglist/search/qmtbbdj/%s"
        for i in xrange(10):
            download_url = url % i
            yield Request(download_url, self.parse)

    def parse(self, response):
        sites = response.xpath('//div[@class="main-list"]/ul/li/a/@href').extract()
        for site in sites:
            yield Request(site, callback=self.parse_item)


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
