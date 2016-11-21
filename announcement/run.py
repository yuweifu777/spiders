import os

commands = ['scrapy crawl cninfosz', 'scrapy crawl cninfosh']

for command in commands:
    os.system(command)