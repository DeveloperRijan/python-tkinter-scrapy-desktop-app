import scrapy
from scrapy import signals

class DownimageSpider(scrapy.Spider):
    name = 'downimage'
    
    def __init__(self, filename=None):
        if filename:
            with open(filename, 'r') as f:
                self.start_urls = f.readlines()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(DownimageSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider


    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)


    def parse(self, response):
        row_image_urls = response.css('img ::attr(src)').getall()
        clean_image_urls = []

        for img_url in row_image_urls:
        	clean_image_urls.append(response.urljoin(img_url))

        yield{
        	"image_urls":clean_image_urls
        }
    
    #call the method to track processing is finished
    print("Scrapy Process Finished")