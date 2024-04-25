import qbittorrent
import json
from utils import ROOT_DIR
import os

CONFIG_PATH = os.path.join(ROOT_DIR, 'qb_pref.json')


class QbWrapper(qbittorrent.Client):
    def __init__(self):
        super().__init__(url="http://127.0.0.1:8080/")
        # = Client("http://127.0.0.1:8080/")
        self.login("admin", "adminadmin")
        self.torrent_index = ""
        self.active_torrent = ""
        self.progress = ""
        with open(CONFIG_PATH, 'r') as preferences:
            self.set_preferences(**json.load(preferences))

    def download(self, magnet):
        self.download_from_link(magnet)
        hash = self.get_hash(magnet)
        # self.toggle_sequential_download([hash])
        torrents = self.torrents()
        active_torrent_index=""
        for i, torrent in enumerate(self.torrents()):
            if self.get_hash(torrent["magnet_uri"]) == self.get_hash(magnet):
                self.torrent_index=i
                # self.toggle_sequential_download(self.torrents()[i]["infohash_v1"])
                self.toggle_first_last_piece_priority(self.torrents()[i]["infohash_v1"])
                break

    def stop(self):
        print("stopping torrent")
        self.pause_all()

    def is_complete(self):
        return (
            self.torrents()[self.torrent_index]["completed"]
            / self.torrents()[self.torrent_index]["total_size"]
        ) == 1

    def get_raw_progress(self):
        return self.progress

    def show_progress(self):
        self.active_torrent = self.torrents()[int(self.torrent_index)]
        progress = (
            self.active_torrent["completed"] / self.active_torrent["total_size"]
        ) * 100
        bar = list("[")
        for i in range(1, 101):
            if i <= progress:
                bar.append("#")
            else:
                bar.append("_")
        bar.append("]")
        bar[round(progress)] = "#"
        print(
            "Download {0} is at {1:.0f}% \n {2}".format(
                self.active_torrent["name"], progress, "".join(bar)
            ),
        )
        self.progress = progress

    def get_hash(self, magnet):
        return magnet.split("&")[0].upper()
