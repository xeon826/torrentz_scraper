```
sudo add-apt-repository ppa:qbittorrent-team/qbittorrent-stable
sudo apt install qbittorrent
```
Enable the webui.
Make sure qbittorrent is running.
```
cp qb_pref.template.json qb_pref.json
```
Omit any preferences you don't plan on changing.
```
pip install -r requirements.txt
python main.py
```
