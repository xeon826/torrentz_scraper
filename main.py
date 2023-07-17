import os

# from pymp4.parser import Box, BoxReader, MovieHeaderBox
import subprocess
import sys
from threading import Event

from scrapy.crawler import CrawlerProcess
from tabulate import tabulate
from termcolor import colored

from qbwrapper import QbWrapper
from spider import MySpider

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
torrent = QbWrapper()


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
        magnet = results[int(selection)]["magnet"][0]
        torrent.download(magnet)
        playing = False
        downloading_sequentially = False
        while not exit.is_set():
            torrent.show_progress()
            exit.wait(1)
            clear = lambda: os.system("clear")
            clear()
            if torrent.get_raw_progress() > 40 and not playing:
                subprocess.run(
                    # 'nohup mpv "%s" --profile=low-latency --log-file=output.txt &'
                    'nohup mpv "%s" --log-file=output.txt &'
                    % torrent.active_torrent["content_path"],
                    shell=True,
                )
                playing = True
                print("playing " + str(playing))
            if torrent.get_raw_progress() > 10 and not downloading_sequentially:
                torrent.toggle_sequential_download(
                    torrent.active_torrent["infohash_v1"]
                )
                torrent.toggle_first_last_piece_priority(
                    torrent.active_torrent["infohash_v1"]
                )
                downloading_sequentially = True
            if torrent.is_complete():
                torrent.stop()
                break
    process.stop()


# def has_moov_atom(file_path):
#     with open(file_path, 'rb') as f: #todo pass file path here
#         reader = BoxReader(f)
#         root = reader.read()
#     moov_box = None

#     for box in root.children:
#         if box.type == 'moov':
#             moov_box = box
#             break

#     if moov_box:
#         # Perform validation on the moov atom
#         # You can access and check its child boxes, metadata, and structure
#         # For example, you can check if it contains necessary boxes like 'mvhd' (MovieHeaderBox)
#         if any(isinstance(child, MovieHeaderBox) for child in moov_box.children):
#             return True # moov atom present and valid
#         else:
#             return False # moov atom present but not valid
#     else:
#         return False # moov atom not present


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
