import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider

process = CrawlerProcess(
    {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.15.3 Chrome/87.0.4280.144 Safari/537.36"
    }
)


class MySpider(scrapy.Spider):
    query = input("Query: ")
    custom_settings = {"LOG_ENABLED": False}
    name = "blogspider"
    results = []
    start_urls = ["https://torrentz2.nz/search?q=%s" % str(query)]

    def parse(self, response):
        for i, row in enumerate(response.css(".results > dl")):
            title = row.css("dt > a::text").extract()[0]
            magnet = row.css("dd > span > a::attr('href')").extract()
            size = row.css("dd > span:nth-child(3)::text").extract()[0]
            seeds = row.css("dd > span:nth-child(4)::text").extract()[0]
            leeches = row.css("dd > span:nth-child(5)::text").extract()[0]
            self.results.append(
                {
                    "title": title,
                    "magnet": magnet,
                    "size": size,
                    "seeds": seeds,
                    "leeches": leeches,
                }
            )
            if i >= 50:
                break

    def start(self):
        pass

    def close(self):
        raise CloseSpider()

    # def set_query(self):
    #     self.query = input('Query: ')

    def get_results(self):
        return self.results
