from qbittorrent import Client
import time

class Torrent():
    qb = Client("http://127.0.0.1:8080/")
    qb.login('admin', 'adminadmin')
    qb.download_from_link()

    download(magnet):
        qb.download_from_link(magnet)
        while True:
            print(qb.torrents()[1])
            time.sleep(1)


