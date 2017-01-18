# -*- coding: utf-8 -*-
"""
    News from www.cs.com.cn (Chinese Stock Newspaper)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Each section only provide 10 pages of news, approximately news for 2 weeks

    Divide the spider into  cs and cs2 because the content is a bit different in different section

    2017.1
"""
import sys
import urlparse
import datetime

from scrapy.spiders import Spider
from scrapy.http import Request
from news.items import NewsItem

reload(sys)
sys.setdefaultencoding('utf-8')

class CsSpider(Spider):
    """only provide 10 pages' news:
            ~~~~~~~~~~~~~~~~~~~~~~
        http://www.cs.com.cn/ssgs/gsxw/index.html
        http://www.cs.com.cn/ssgs/gsxw/index_1.html
        http://www.cs.com.cn/ssgs/gsxw/index_2.html
            ......
        http://www.cs.com.cn/ssgs/gsxw/index_9.html
        """
    name = 'cs'
    allowed_domains = ["cs.com.cn"]

    # for test
    # start_urls = ['http://www.cs.com.cn/xwzx/hg/']

    # scrapy for different part, only provide first 10 pages
    def start_requests(self):
        # 1. company news
        url = 'http://www.cs.com.cn/ssgs/gsxw/'
        for i in xrange(0, 10):
            if i is 0:
                download_url = url
                yield Request(download_url, self.parse)
            else:
                download_url = url + "index_%s.html" % i
                yield Request(download_url, self.parse)

        # 2. industry news
        url = 'http://www.cs.com.cn/ssgs/hyzx/'
        for i in xrange(0, 10):
            if i is 0:
                download_url = url
                yield Request(download_url, self.parse)
            else:
                download_url = url + "index_%s.html" % i
                yield Request(download_url, self.parse)

        # 3. macroeconomics
        url = 'http://www.cs.com.cn/xwzx/hg/'
        for i in xrange(0, 10):
            if i is 0:
                download_url = url
                yield Request(download_url, self.parse)
            else:
                download_url = url + "index_%s.html" % i
                yield Request(download_url, self.parse)

        # 4. overseas
        url = 'http://www.cs.com.cn/xwzx/hwxx/'
        for i in xrange(0, 10):
            if i is 0:
                download_url = url
                yield Request(download_url, self.parse)
            else:
                download_url = url + "index_%s.html" % i
                yield Request(download_url, self.parse)

        # 5. market research
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
        item['content'] = response.xpath('//div[@class="Dtext"]').extract_first()
        item['url'] = response.url
        return item