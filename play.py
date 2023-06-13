import scrapy
from scrapy.crawler import CrawlerProcess

# query = "the professional"


class MySpider(scrapy.Spider):
    query = input("Query: ")
    custom_settings = {"LOG_ENABLED": False}
    name = "blogspider"
    results = []
    # start_urls = ['https://torrentz2.nz/search?q=the+ritual']
    start_urls = ["https://torrentz2.nz/search?q=%s" % str(query)]

    def parse(self, response):
        # for href in response.css("dd > span > a::attr('href')").extract():
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
        for i, obj in enumerate(self.results):
            print("%s) %s %s %s" % (str(i), obj["title"], obj["seeds"], obj["leeches"]))
        selection = input('0-20 to select, r to perform new query, x to quit: ')
        if selection == 'r':
            self.query = input('Query: ')
            process.crawl(MySpider)
            process.start()
        elif selection == 'x':
            print('bye')
        else:
            print("selected %s" % self.results[int(selection)]['title'])


process = CrawlerProcess(
    {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.15.3 Chrome/87.0.4280.144 Safari/537.36"
    }
)

process.crawl(MySpider)
process.start()
