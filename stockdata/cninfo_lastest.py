# -*- coding:utf-8 -*-
"""
    simple spider to crawl cninfo announcements
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    test latest, unique mongodb id
"""
import os
import sys
import time
import json
import codecs
import urllib
import datetime
import requests

#: use mongoengine to save the data
from mongoengine import *

reload(sys)
sys.setdefaultencoding('utf-8')

#: query latest announcement
sz_url =  'http://www.cninfo.com.cn/cninfo-new/disclosure/szse_latest' 
s_url =  'http://www.cninfo.com.cn/cninfo-new/disclosure/sse_latest' 


#: store_time
def ts2time(timestamp):
    local_time = time.localtime(timestamp)
    str_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    date_time = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    return date_time


def get_sz():
    
    #: connect to 'cninfo' mongodb database
    connect('cninfo')

    #: Storing with MongoEngine
    #: collection named Daily in cninfo database
    class Latest(Document):
        #: attributes of each document
        time = DateTimeField() 
        secName = StringField()
        secCode = StringField()
        url = StringField(primary_key=True)
        announcementTitle = StringField() 
        announcementTypeName = StringField()
        pageColumn = StringField()
        columnId = StringField()
        
    #: decoding
    columnTitle = urllib.quote("深市公告")

    #: start from page 1
    pageNum = 1

    while True:
        #: post data
        payload = {
            'category ': '',
            'column  ': 'szse',
            'columnTitle ': columnTitle,
            'limit': '',
            'pageNum': pageNum,
            'pageSize': 50,
            'plate':'',
            'seDate':'',
            'searchkey':'',
            'showTitle':'',
            'sortName':'',
            'sortType ':'',
            'stock':'',
            'tabName':'latest',
            'trade':''
        }        
        r = requests.post(sz_url, data=payload)

        # list of dictionary
        if not r.json()['hasMore']:
            break

        anno = r.json()['classifiedAnnouncements']

        for i in anno:
            for j in i:
                new_anno = Latest()
                new_anno.secName = j['secName']
                new_anno.secCode = j['secCode']
                new_anno.time = ts2time(j['storageTime'] / 1000.0)        
                new_anno.announcementTitle = j['announcementTitle']
                new_anno.announcementTypeName = j['announcementTypeName']
                new_anno.url = 'http://www.cninfo.com.cn/' + j['adjunctUrl']                
                new_anno.save()
        print "Finish SZ pageNum: ", pageNum
        pageNum += 1
        #: testing with only one page
        # break
        
def get_s():
    
    #: connect to 'cninfo' mongodb database
    connect('cninfo')

    #: Storing with MongoEngine
    #: collection named Daily in cninfo database
    class Latest(Document):
        #: attributes of each document
        time = DateTimeField() 
        secName = StringField()
        secCode = StringField()
        url = StringField()
        announcementTitle = StringField() 
        announcementTypeName = StringField()
        pageColumn = StringField()
        columnId = StringField()

    #: decoding
    columnTitle = urllib.quote("沪市公告")

    #: start from page 1
    pageNum = 1

    while True:
        #: post data
        payload = {
            'category ': '',
            'column  ': 'sse',
            'columnTitle ': columnTitle,
            'limit': '',
            'pageNum': pageNum,
            'pageSize': 50,
            'plate':'',
            'seDate':'',
            'searchkey':'',
            'showTitle':'',
            'sortName':'',
            'sortType ':'',
            'stock':'',
            'tabName':'latest',
            'trade':''
        }        
        r = requests.post(s_url, data=payload)

        # list of dictionary
        if not r.json()['hasMore']:
            break

        anno = r.json()['classifiedAnnouncements']

        for i in anno:
            for j in i:
                new_anno = Latest()
                new_anno.secName = j['secName']
                new_anno.secCode = j['secCode']
                new_anno.time = ts2time(j['storageTime'] / 1000.0)        
                new_anno.announcementTitle = j['announcementTitle']
                new_anno.announcementTypeName = j['announcementTypeName']
                new_anno.url = 'http://www.cninfo.com.cn/' + j['adjunctUrl']
                new_anno.save()
        print "Finish S pageNum: ", pageNum
        pageNum += 1
        #: testing with only one page
        # break
        


if __name__ == '__main__':
    get_sz()
    get_s()