import scrapy


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://torrentz2.nz/search?q=the+ritual']

    def parse(self, response):
        for href in response.css("dd > span > a::attr('href')").extract():
            print(href)
