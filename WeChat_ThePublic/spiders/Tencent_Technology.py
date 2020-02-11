# -*- coding: utf-8 -*-
import scrapy
import json
from Utils import *
from WeChat_ThePublic.items import NewsItem
import datetime


class TencentTechnologySpider(scrapy.Spider):
    name = 'Tencent_Technology'
    allowed_domains = ['qq.com']
    start_urls = ['https://pacaio.match.qq.com/irs/rcd?cid=146&token=49cbb2154853ef1a74ff4e53723372ce&ext=tech&page=0']
    urls_crawled = set()

    def parse(self, response):
        article_list = json.loads(response.text)["data"]
        for article in article_list:
            url = article["vurl"]
            publish_time = article["publish_time"]
            if date_limit(publish_time) and (url not in self.urls_crawled):
                yield scrapy.Request(url, callback=self.article_parse)
                self.urls_crawled.add(url)

        if response._get_url() in self.start_urls:
            url_format = self.start_urls[0].rstrip("0")
            for i in range(1, 6):
                url = url_format + i.__str__()
                yield scrapy.Request(url, callback=self.parse)

    def article_parse(self, response):
        url = response._get_url()
        title = response.xpath("//div[@class='LEFT']/h1/text()").get()
        keywords = response.xpath("//meta[@name='keywords']/@content").get()
        author = " "
        published_time = response.xpath("//meta[@name='apub:time']/@content").get()
        if published_time != None:
            published_time = datetime.datetime.strptime(published_time, "%Y-%m-%d %H:%M:%S")
        content_list = response.xpath("//div[@class='content-article']//p/text()").getall()
        content = "\n".join(content_list).strip()
        picture_url_list = response.xpath("//div[@class='content-article']//img/@src").getall()

        newsItem = NewsItem(url=url, published_time=published_time, title=title, keywords=keywords, author=author,
                            content=content, picture_url_list=picture_url_list)
        self.urls_crawled.add(url)
        if title != None:
            yield newsItem