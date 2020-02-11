from scrapy import cmdline
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from Utils import Exportor
import os


# cmdline.execute("scrapy crawl NetEase_Technology".split())     # 应该是接受一个列表
# cmdline.execute("scrapy crawl sina_Technology".split())
# cmdline.execute("scrapy crawl Tencent_Technology".split())

def main():
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    didntWorkSpider = ['']

    for spider_name in process.spiders.list():
        if spider_name in didntWorkSpider :
            continue
        print("Running spider %s" % (spider_name))
        process.crawl(spider_name)
    process.start()

if __name__ == '__main__':
    os.remove("./data/WeChat_ThePublic.db")
    main()
    ex = Exportor()
    ex.export_docx()
    os.system("start explorer D:\Project\WeChat_ThePublic\data")
    # os.system("start explorer .\data")        #360拦截？？
