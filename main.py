import os
import subprocess
import sys
import time
from subprocess import Popen
from threading import Event

from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
from tabulate import tabulate
from termcolor import colored, cprint

from play import MySpider
from torrent import Torrent

# vpn_is_running = "Connected" in subprocess.check_output(
#     'nordvpn status | grep "Status"', shell=True, text=True
# )
# if not vpn_is_running:
#     print("VPN is not running")
#     sys.exit()

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
    results = spider.get_results()
    results_as_list = []
    for i, result in enumerate(results):
        if i % 2 == 0:
            row_color = "yellow"
        else:
            row_color = "blue"
        obj = [
            colored(str(i) + ")__", row_color, attrs=["bold", "reverse"]),
            colored(result["title"], row_color, attrs=["bold", "reverse"]),
            colored(result["desc"], row_color, attrs=["bold"]),
            colored(result["seeds"], "green", attrs=["underline"]),
            colored(result["leeches"], "blue", attrs=["underline"]),
        ]
        results_as_list.append(obj)
    print(
        tabulate(
            results_as_list,
            headers=["Option", "Title", "Desc", "Seeds", "Leeches"],
            tablefmt="outline",
        )
    )

    selection = input(
        "0-%s to select, r to perform new query, x to quit: " % str(len(results) - 1)
    )
    if selection == "x":
        sys.exit()
    else:
        torrent.download(results[int(selection)]["magnet"][0])
        playing = False
        while not exit.is_set():
            torrent.show_progress()
            exit.wait(1)
            clear = lambda: os.system("clear")
            clear()
            if torrent.get_raw_progress() > 15 and not playing:
                subprocess.run(
                    'nohup mpv "%s" &' % torrent.active_torrent["content_path"],
                    shell=True,
                )
                playing = True
                print("playing " + str(playing))
            if torrent.is_complete():
                torrent.stop()
                break
    process.stop()


def quit(signo, _frame):
    print("Interrupted by %d, shutting down" % signo)
    torrent.stop()
    exit.set()
    sys.exit()


if __name__ == "__main__":
    import signal

    for sig in ("TERM", "HUP", "INT"):
        signal.signal(getattr(signal, "SIG" + sig), quit)

    main()
