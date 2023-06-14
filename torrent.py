import time
import re

from clint.textui import progress
from qbittorrent import Client


class Torrent:
    qb = Client("http://127.0.0.1:8080/")
    qb.login("admin", "adminadmin")
    torrent_index = ""
    stop = False
    active_torrent = ''
    progress = ''
    # qb.download_from_link()

    def download(self, magnet):
        self.qb.download_from_link(magnet, savepath='/media/dan/My Passport/movies/')
        # print(self.qb.torrents()[-1])
        torrents = self.qb.torrents()
        active_torrent_index = ""
        for i, torrent in enumerate(self.qb.torrents()):
            if self.get_hash(torrent["magnet_uri"]) == self.get_hash(magnet):
                self.torrent_index = i
                break

    def stop(self):
        print('stopping torrent')
        self.qb.pause_all()

    def is_complete(self):
        return (
            self.qb.torrents()[self.torrent_index]["completed"]
            / self.qb.torrents()[self.torrent_index]["total_size"]
        ) == 1

    def get_raw_progress(self):
        return self.progress

    def show_progress(self):
        self.active_torrent = self.qb.torrents()[self.torrent_index]
        progress = ((self.active_torrent["completed"] / self.active_torrent["total_size"]) * 100)
        bar = list('[')
        for i in range(1, 101):
            if i <= progress:
                bar.append('#')
            else:
                bar.append('_')
        bar.append(']')
        bar[round(progress)] = '#'
        print(
            "Download {0} is at {1:.0f}% \n {2}".format(
                self.active_torrent["name"], progress, ''.join(bar)
            ),
        )
        self.progress = progress

    def get_hash(self, magnet):
        return magnet.split("&")[0].upper()

        # for torrent in self.qb.torrents():
        #     if torrent['magnet_uri'] == magnet:
        #         print('IF')
        #         while torrent['amount_left'] != 0:
        #             print('WHILE')
        #             print((torrent['completed'] / torrent['completion_on']) * 100 + '% done')
        #             time.sleep(1)
