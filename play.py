import scrapy
from scrapy.crawler import CrawlerProcess

# query = "the professional"


class MySpider(scrapy.Spider):
    query = input("Query: ")
    # custom_settings = {"LOG_ENABLED": False}
    name = "blogspider"
    results = []
    # start_urls = ['https://torrentz2.nz/search?q=the+ritual']
    start_urls = ["https://torrentz2.nz/search?q=%s" % str(query)]

    def parse(self, response):
        for i, row in enumerate(response.css(".results > dl")):
            title = row.css("dt > a::text").extract()[0]
            magnet = row.css("dd > span > a::attr('href')").extract()
            seeds = row.css("dd > span:nth-child(4)::text").extract()[0]
            leeches = row.css("dd > span:nth-child(5)::text").extract()[0]
            self.results.append(
                {"title": title, "magnet": magnet, "seeds": seeds, "leeches": leeches}
            )
            if i >= 20:
                break

    def get_results(self):
        return self.results



