# -*- coding: utf-8 -*-
from WeChat_ThePublic.items import NewsItem
from Utils import *
import scrapy
import json
from json import JSONDecodeError
import re
import datetime

class NeteaseTechnologySpider(scrapy.Spider):
    name = 'NetEase_Technology'
    allowed_domains = ['163.com']
    start_urls = ['http://tech.163.com/gd/','https://tech.163.com/special/00097UHL/tech_datalist.js?callback=data_callback',
                  'https://tech.163.com/special/00097UHL/tech_datalist_02.js?callback=data_callback',
                  'https://tech.163.com/special/00097UHL/tech_datalist_03.js?callback=data_callback']
    urls_crawled = set()

    def parse(self, response):
        print(response._get_url())
        if response._get_url() in self.start_urls[1:-1]:
            content = response.text.encode(response.encoding).decode('gbk').replace("data_callback(", "").replace(")","")
            try:
                articles_list = json.loads(content)
            except JSONDecodeError:
                print(content)
            for item in articles_list:
                url = item["docurl"]
                title = item["title"]
                yield scrapy.Request(url, callback=self.article_parse)
                self.urls_crawled.add(url)

        else:
            article_selectors = response.xpath("//ul[@class='newsList']//li")
            for i, selector in enumerate(article_selectors):
                webPage = selector.get()
                url = re.findall(r"https://tech\.163\.com.*\.html", webPage)[0]
                title = re.findall(r"html\">.*</a></h3>", webPage)[0].replace("html\">", "").replace("</a></h3>", "")
                published_time = re.findall(r"\d+-\d+-\d+ \d+:\d+:\d+", webPage)[0]
                # url = selector.xpath("//h3[@class='bigsize ']/a/@href").getall()[i]
                # self.url_pic[url] = selector.xpath("//a[@class='newsList-img']/img/@src").getall()[i]
                # published_time = selector.xpath("//p[@class='sourceDate']/text()").getall()[i]
                if date_limit(published_time)and (url not in self.urls_crawled):
                    yield scrapy.Request(url, callback=self.article_parse)
                    self.urls_crawled.add(url)

            # 从第一页提取所有页面的网页URL
            if response.xpath("//div[@class='pages']/span/text()").get() == '<':
                next_page_urls = response.xpath("//div[@class='pages']/a/@href").getall()
                for url in next_page_urls:
                    yield scrapy.Request(url, callback=self.parse)

    def article_parse(self, response):
        url = response._get_url()
        title = response.xpath("//div[@class='post_content_main']/h1/text()").get()
        keywords = response.xpath("//meta[@name='keywords']/@content").get()
        author = response.xpath("//meta[@name='author']/@content").get()
        published_time_o = response.xpath("//meta[@property='article:published_time']/@content").get()
        published_time = published_time_o.replace("T"," ").split("+")[0]
        if published_time != None:
            published_time = datetime.datetime.strptime(published_time, "%Y-%m-%d %H:%M:%S")
        content_list = response.xpath("//div[@class='post_text']//p/text()").getall()
        content = "\n".join(content_list).strip()
        picture_url_list = response.xpath("//div[@class='post_text']//img/@src").getall()

        newsItem = NewsItem(url=url, published_time=published_time, title=title, keywords=keywords, author=author, content=content, picture_url_list=picture_url_list)
        self.urls_crawled.add(url)
        if title != None:
            yield newsItem

