# -*- coding: utf-8 -*-

import os
import codecs
from scrapy.spiders import Spider
from scrapy.http import Request
from ..items import ReportItem


class ReportSpider(Spider):
    name = "report"
    allowed_domains = ["chuansong.me"]
    headers = {
        "Host": "chuansong.me",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0"
    }

    def start_requests(self):
        with codecs.open(os.getcwd()+'/report/spiders/analysts.txt', 'r', 'utf-8') as f:
            analysts = f.readlines()
        for analyst in analysts:
            yield Request(url=analyst.split(' ')[1][:-1], headers=self.headers, callback=self.parse)

    def parse(self, response):
        # sites[0] =  u'/n/804697551251'
        sites = response.xpath('//div[@class="feed_item_question"]/h2/span/a/@href').extract()
        for site in sites:
            # url = http://chuansong.me/n/804697551251
            url = 'http://chuansong.me' + site
            yield Request(url=url, headers=self.headers, callback=self.parse_item)
        # check for pagination
        next_page = response.xpath('//a[@style="float: right"]/@href').extract_first()
        if next_page is not None:
            next_page = 'http://chuansong.me' + next_page
            yield Request(url=next_page, headers=self.headers, callback=self.parse)

    def parse_item(self, response):
        item = ReportItem()
        item['title'] = response.xpath('//h2[@id="activity-name" and '
                                       '@class="rich_media_title"]/text()').extract_first().strip()
        item['time'] = response.xpath('//em[@id="post-date"]/text()').extract_first()
        item['analyst'] = response.xpath('//a[@id="post-user"]/text()').extract_first()
        item['content'] = response.xpath('//div[@id="img-content" and '
                                         '@class="rich_media_area_primary"]').extract_first()
        yield item
