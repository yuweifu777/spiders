import os

commands = [
    'scrapy crawl cs',
    'scrapy crawl cs2',
    'scrapy crawl cnstock',
    'scrapy crawl stcn'
]

for command in commands:
    os.system(command)