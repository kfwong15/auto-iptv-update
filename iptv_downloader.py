# iptv_downloader.py

import requests

URL = "https://raw.githubusercontent.com/iptv-org/iptv/master/index.m3u"
OUTPUT = "iptv_all.m3u"

def download():
    print(f"Downloading from: {URL}")
    r = requests.get(URL)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(r.text)
    print(f"Saved to {OUTPUT}")

if __name__ == "__main__":
    download()
