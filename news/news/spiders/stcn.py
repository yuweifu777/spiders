# -*- coding: utf-8 -*-
import sys
import datetime

from scrapy.spiders import Spider
from scrapy.http import Request
from news.items import NewsItem

reload(sys)
sys.setdefaultencoding('utf-8')

class StcnSpider(Spider):
    name = "stcn"
    allowed_domains = ["stcn.com"]
    #: hot spot company
    start_urls = [
        "http://company.stcn.com/gsxw/index.shtml",
        "http://company.stcn.com/cjnews/index.shtml",
        "http://company.stcn.com/xinsanban/index.shtml",
        "http://stock.stcn.com/dapan/index.shtml",
        "http://stock.stcn.com/bankuai/index.shtml",
        "http://stock.stcn.com/zhuli/index.shtml",
    ]

    def parse(self, response):
        sites = response.xpath('//div[@id="mainlist" and @class="mainlist"]/ul/li/p/a/@href').extract()
        for site in sites:
            yield Request(site, callback=self.parse_item)
        next_url = response.xpath('//div[@class="pagelist"]/ul/li/a[@class="next"]/@href').extract_first()
        if next_url is not None:
            yield Request(next_url, callback=self.parse)

    def parse_item(self, response):
        item = NewsItem()
        item['title'] = response.xpath('//div[@class="intal_tit"]/h2/text()').extract_first()
        item['time'] = response.xpath('//div[@class="intal_tit"]/div[@class="info"]/text()').extract_first()[:10]
        item['time'] = datetime.datetime.strptime(item['time'], '%Y-%m-%d')
        item['content'] = response.xpath('//div[@id="ctrlfscont" and @class="txt_con"]').extract_first()
        if item['content'] is not None:
            item['content'] = item['content']
        item['url'] = response.url
        yield item
