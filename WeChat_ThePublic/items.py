# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WechatThepublicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewsItem(scrapy.Item):
    url = scrapy.Field()
    published_time = scrapy.Field()
    title = scrapy.Field()
    keywords = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    picture_url_list = scrapy.Field()

