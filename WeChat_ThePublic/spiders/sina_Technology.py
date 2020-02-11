# -*- coding: utf-8 -*-
import scrapy
import re
import datetime, time
from WeChat_ThePublic.items import NewsItem


class SinaTechnologySpider(scrapy.Spider):
    name = 'sina_Technology'
    allowed_domains = ['sina.com.cn', 'sina.cn']
    start_urls = ['https://cre.mix.sina.com.cn/api/v3/get?callback=jQuery111208139140384781385_1580717080418&cateid=1z&cre=tianyi&mod=pctech']
    urls_crawled = set()

    def parse(self, response):
        content = response.text.encode(response.encoding).decode('utf-8')
        url_list = re.findall(r"http://tech\.sina\.cn/.*?\.html", content)
        title_list = re.findall(r"\"title\":\".*?\"", content)
        for url in url_list:
            if url not in self.urls_crawled:
                yield scrapy.Request(url, callback=self.article_parse)
                self.urls_crawled.add(url)

        if response._get_url() in self.start_urls:
            stamp_datetime = datetime.datetime.now()
            for i in range(4, 48, 4):
                timestamp1 = stamp_datetime + datetime.timedelta(hours=-i)
                timestamp1 = int(time.mktime(timestamp1.timetuple()))
                timestamp2 = int(time.mktime(stamp_datetime.timetuple()))*1000 + 333
                url = self.start_urls[0] + "&ctime=" + timestamp1.__str__() + "&_=" + timestamp2.__str__()
                yield scrapy.Request(url, callback=self.parse)

    def article_parse(self, response):
        url = response._get_url()
        title = response.xpath("//article[@class='art_box']/h1/text()").get()
        keywords = response.xpath("//meta[@name='keywords']/@content").get()
        author = response.xpath("//meta[@name='author']/@content").get()
        published_time = response.xpath("//meta[@property='article:published_time']/@content").get()
        if published_time != None:
            published_time = datetime.datetime.strptime(published_time, "%Y-%m-%d %H:%M:%S")
        content_list = response.xpath("//article[@class='art_box']//p/text()").getall()
        content = "\n".join(content_list).strip()
        picture_url_list = response.xpath("//article[@class='art_box']//img/@src").getall()

        newsItem = NewsItem(url=url, published_time=published_time, title=title, keywords=keywords, author=author,content=content, picture_url_list=picture_url_list)
        self.urls_crawled.add(url)
        if title != None:
            yield newsItem
