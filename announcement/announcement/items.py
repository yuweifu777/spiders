# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class AnnouncementItem(Item):
    time = Field()
    secName = Field()
    secCode = Field()
    url = Field()
    announcementTitle = Field()
    announcementTypeName = Field()

