# -*- coding: utf-8 -*-
"""
    lastest announcement from www.cninfo.com
"""
import json
import time
import urllib
import datetime
from scrapy import FormRequest
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from announcement.items import AnnouncementItem


#: store_time
def ts2time(timestamp):
    local_time = time.localtime(timestamp)
    str_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    date_time = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    return date_time

class CninfoszSpider(Spider):
    name = "cninfosz"
    allowed_domains = ["cninfo.com.cn"]
    url = 'http://www.cninfo.com.cn/cninfo-new/disclosure/szse_latest'
    columnTitle = urllib.quote("深市公告")
    pageNum = 1
    formdata = {
        'category': '',
        'column': 'szse',
        'columnTitle': columnTitle,
        'limit': '',
        'pageNum': str(pageNum),
        'pageSize': '50',
        'plate': '',
        'seDate': '',
        'searchkey': '',
        'showTitle': '',
        'sortName': '',
        'sortType': '',
        'stock': '',
        'tabName': 'latest',
        'trade': ''
    }

    def start_requests(self):
        yield FormRequest(
            self.url,
            formdata=self.formdata,
            callback=self.parse_item,
        )

    def parse_item(self, response):
        jsonbody = json.loads(response.body)
        anno = jsonbody['classifiedAnnouncements']
        for i in anno:
            for j in i:
                item = AnnouncementItem()
                item['secName'] = j['secName']
                item['secCode'] = j['secCode']
                item['time'] = ts2time(j['storageTime']/1000.0)
                item['announcementTitle'] = j['announcementTitle']
                item['announcementTypeName'] = j['announcementTypeName']
                item['url'] = 'http://www.cninfo.com.cn/'+j['adjunctUrl']
                yield item

        if jsonbody['hasMore'] is True:
            self.pageNum += 1
            self.formdata['pageNum'] = str(self.pageNum)
            yield FormRequest(
                self.url,
                formdata=self.formdata,
                callback=self.parse_item,
            )


class CninfoshSpider(Spider):
    name = "cninfosh"
    allowed_domains = ["cninfo.com.cn"]
    url = 'http://www.cninfo.com.cn/cninfo-new/disclosure/sse_latest'
    columnTitle = urllib.quote("沪市公告")
    pageNum = 1
    formdata = {
        'category': '',
        'column': 'sse',
        'columnTitle': columnTitle,
        'limit': '',
        'pageNum': str(pageNum),
        'pageSize': '50',
        'plate': '',
        'seDate': '',
        'searchkey': '',
        'showTitle': '',
        'sortName': '',
        'sortType': '',
        'stock': '',
        'tabName': 'latest',
        'trade': ''
    }

    def start_requests(self):
        yield FormRequest(
            self.url,
            formdata=self.formdata,
            callback=self.parse_item,
        )

    def parse_item(self, response):
        jsonbody = json.loads(response.body)
        anno = jsonbody['classifiedAnnouncements']
        for i in anno:
            for j in i:
                item = AnnouncementItem()
                item['secName'] = j['secName']
                item['secCode'] = j['secCode']
                item['time'] = ts2time(j['storageTime']/1000.0)
                item['announcementTitle'] = j['announcementTitle']
                item['announcementTypeName'] = j['announcementTypeName']
                item['url'] = 'http://www.cninfo.com.cn/'+j['adjunctUrl']
                yield item

        if jsonbody['hasMore'] is True:
            self.pageNum += 1
            self.formdata['pageNum'] = str(self.pageNum)
            yield FormRequest(
                self.url,
                formdata=self.formdata,
                callback=self.parse_item,
            )

