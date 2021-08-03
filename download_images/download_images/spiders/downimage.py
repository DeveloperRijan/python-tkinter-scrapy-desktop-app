import scrapy


class DownimageSpider(scrapy.Spider):
    name = 'downimage'
    #allowed_domains = ['example.com']
    start_urls = ['https://pakistaniexports.com/']

    def parse(self, response):
        row_image_urls = response.css('img ::attr(src)').getall()
        clean_image_urls = []

        for img_url in row_image_urls:
        	clean_image_urls.append(response.urljoin(img_url))

        yield{
        	"image_urls":clean_image_urls
        }
