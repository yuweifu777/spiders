# -*- coding: utf-8 -*-
import sys
import urlparse
import datetime

from scrapy.spiders import Spider
from scrapy.http import Request
from news.items import NewsItem

reload(sys)
sys.setdefaultencoding('utf-8')


class CsSpider(Spider):
    name = "cs"
    allowed_domains = ["cs.com.cn"]
    # for test
    # start_urls = ['http://www.cs.com.cn/xwzx/hg/']

    # scrapy for different part, only provide first 10 pages
    def start_requests(self):

        # company news
        url = 'http://www.cs.com.cn/ssgs/gsxw/'
        for i in xrange(0, 10):
            if i is 0:
                download_url = url
                yield Request(download_url, self.parse)
            else:
                download_url = url + "index_%s.html" % i
                yield Request(download_url, self.parse)

        # industry news
        url = 'http://www.cs.com.cn/ssgs/hyzx/'
        for i in xrange(0, 10):
            if i is 0:
                download_url = url
                yield Request(download_url, self.parse)
            else:
                download_url = url + "index_%s.html" % i
                yield Request(download_url, self.parse)

        # market research
        url = 'http://www.cs.com.cn/gppd/scyj/'
        for i in xrange(0, 10):
            if i is 0:
                download_url = url
                yield Request(download_url, self.parse)
            else:
                download_url = url + "index_%s.html" % i
                yield Request(download_url, self.parse)


    def parse(self, response):
        sites = response.xpath('//div[@class="column-box"]/ul/li/a/@href').extract()
        for url in sites:
            yield Request(urlparse.urljoin(response.url, url),
                          callback=self.parse_item)


    def parse_item(self, response):
        item = NewsItem()
        item['title'] = response.xpath('//div[@class="column-box"]/h1/text()').extract_first()
        item['time'] = response.xpath('//span[@class="ctime01"]/text()').extract_first()[:10]
        item['time'] = datetime.datetime.strptime(item['time'], '%Y-%m-%d')
        item['content'] = response.xpath('//div[@class="Dtext z_content"]').extract_first()
        item['url'] = response.url
        return item


class CsSpidertwo(Spider):
    name = 'cs2'
    allowed_domains = ["cs.com.cn"]

    # for test
    # start_urls = ['http://www.cs.com.cn/xwzx/hg/']

    # scrapy for different part, only provide first 10 pages
    def start_requests(self):
        # macroeconomics
        url = 'http://www.cs.com.cn/xwzx/hg/'
        for i in xrange(0, 10):
            if i is 0:
                download_url = url
                yield Request(download_url, self.parse)
            else:
                download_url = url + "index_%s.html" % i
                yield Request(download_url, self.parse)

        # overseas
        url = 'http://www.cs.com.cn/xwzx/hwxx/'
        for i in xrange(0, 10):
            if i is 0:
                download_url = url
                yield Request(download_url, self.parse)
            else:
                download_url = url + "index_%s.html" % i
                yield Request(download_url, self.parse)


    def parse(self, response):
        sites = response.xpath('//div[@class="column-box"]/ul/li/a/@href').extract()
        for url in sites:
            yield Request(urlparse.urljoin(response.url, url),
                          callback=self.parse_item)

    def parse_item(self, response):
        item = NewsItem()
        item['title'] = response.xpath('//div[@class="column-box"]/h1/text()').extract_first()
        item['time'] = response.xpath('//span[@class="ctime01"]/text()').extract_first()[:10]
        item['time'] = datetime.datetime.strptime(item['time'], '%Y-%m-%d')
        item['content'] = response.xpath('//div[@class="Dtext"]').extract_first()
        item['url'] = response.url
        return item