from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
import time
from threading import Event
from play import MySpider
from torrent import Torrent

exit = Event()
process = CrawlerProcess(
    {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.15.3 Chrome/87.0.4280.144 Safari/537.36"
    }
)


spider = MySpider()
process.crawl(spider.__class__)
process.start()

def main():
    while not exit.is_set():
        results = spider.get_results()
        for i, obj in enumerate(results):
            print("%s) %s %s %s" % (str(i), obj["title"], obj["seeds"], obj["leeches"]))

        selection = input('0-20 to select, r to perform new query, x to quit: ')
        if selection == 'x':
            print('bye')
            break
        else:
            torrent = Torrent()
            torrent.download(results[int(selection)]['magnet'][0])
            while not exit.is_set():
                torrent.show_progress()
                exit.wait(1)
            break
        process.stop()
        exit.wait(1)


def quit(signo, _frame):
    print("Interrupted by %d, shutting down" % signo)
    exit.set()


if __name__ == '__main__':
    import signal
    print('MAIN')
    for sig in ('TERM', 'HUP', 'INT'):
        signal.signal(getattr(signal, 'SIG'+sig), quit)

    main()
