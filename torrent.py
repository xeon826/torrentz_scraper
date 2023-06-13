from qbittorrent import Client
import time

qb = Client("http://127.0.0.1:8080/")
qb.login('admin', 'adminadmin')
qb.download_from_link('magnet:?xt=urn:btih:2117A0A5C7A53A25163152C77EAB431C7C1D9F4E&tr=udp%3A%2F%2Ftracker.bitsearch.to%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker2.dler.com%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.breizh.pm%3A6969%2Fannounce&tr=udp%3A%2F%2Fwww.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&dn=%5BBitsearch.to%5D+The.Ritual.Killer.2023.1080p.WEBRip.x265-RARBG')


while True:
    print(qb.torrents()[1])
    time.sleep(1)


