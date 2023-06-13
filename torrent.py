import time

from clint.textui import progress
from qbittorrent import Client


class Torrent:
    qb = Client("http://127.0.0.1:8080/")
    qb.login("admin", "adminadmin")
    torrent_index = ''
    stop = False
    # qb.download_from_link()

    def download(self, magnet):
        self.qb.download_from_link(magnet)
        # print(self.qb.torrents()[-1])
        torrents = self.qb.torrents()
        active_torrent_index = ""
        for i, torrent in enumerate(self.qb.torrents()):
            if self.get_hash(torrent["magnet_uri"]) == self.get_hash(magnet):
                self.torrent_index = i
                break

    def stop(self):
        self.stop = True

    def show_progress(self):
        print(
            "%s %",
            str(
                (
                    self.qb.torrents()[self.torrent_index]["completed"]
                    / self.qb.torrents()[self.torrent_index]["total_size"]
                )
                * 100
            ),
        )

    def get_hash(self, magnet):
        return magnet.split("&")[0].upper()

        # for torrent in self.qb.torrents():
        #     if torrent['magnet_uri'] == magnet:
        #         print('IF')
        #         while torrent['amount_left'] != 0:
        #             print('WHILE')
        #             print((torrent['completed'] / torrent['completion_on']) * 100 + '% done')
        #             time.sleep(1)
