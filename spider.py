import scrapy
import unicodedata
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
    start_urls = ["https://thepiratebay0.org/search/%s" % str(query)]

    def parse(self, response):
        for i, row in enumerate(response.css("table#searchResult > tr")):
            title = row.css("td:nth-child(2) > div > a::text").extract()[0]
            if len(title) == 0:
                continue
            magnet = row.css("td:nth-child(2) > a::attr('href')").extract()
            desc = row.css("font.detDesc::text").extract()[0].encode('ascii', 'replace')
            seeds = row.css("td:nth-child(3)::text").extract()[0]
            leeches = row.css("td:nth-child(4)::text").extract()[0]
            self.results.append(
                {
                    "title": title,
                    "magnet": magnet,
                    "desc": desc,
                    "seeds": seeds,
                    "leeches": leeches,
                }
            )
            if i >= 50:
                break

    def start(self):
        pass

    def get_results(self):
        return self.results
