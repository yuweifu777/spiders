# -*- coding:utf-8 -*-
"""
    script to crawl news from three different websites
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import os

commands = [
    'scrapy crawl cs',
    'scrapy crawl cnstock',
    'scrapy crawl stcn'
]

for command in commands:
    os.system(command)