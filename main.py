import os
import sys
import subprocess
# from subprocess import call
import time
from threading import Event

from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider

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
torrent = Torrent()


def main():
    while not exit.is_set():
        results = spider.get_results()
        for i, obj in enumerate(results):
            print("%s) %s %s %s" % (str(i), obj["title"], obj["seeds"], obj["leeches"]))

        selection = input("0-20 to select, r to perform new query, x to quit: ")
        if selection == "x":
            print("bye")
            break
        else:
            torrent.download(results[int(selection)]["magnet"][0])
            playing = False
            while not exit.is_set():
                torrent.show_progress()
                exit.wait(1)
                clear = lambda: os.system("clear")
                clear()
                playing = False
                if torrent.get_raw_progress() > 10 and not playing:
                    subprocess.run('mpv "%s/"' % torrent.active_torrent['content_path'], shell=True)
                    # torrent.stop()
                    # call(['mpv', torrent.active_torrent['content_path']])
                    playing = True
                    print("playing")
                if torrent.is_complete():
                    torrent.stop()
            break
        exit.wait(1)
    process.stop()


def quit(signo, _frame):
    print("Interrupted by %d, shutting down" % signo)
    torrent.stop()
    exit.set()


if __name__ == "__main__":
    import signal

    print("MAIN")
    for sig in ("TERM", "HUP", "INT"):
        signal.signal(getattr(signal, "SIG" + sig), quit)

    main()
