# iptv_downloader.py

import requests
import os

# IPTV-org 最新有效源（按语言）
LANG_URLS = {
    "中文": "https://iptv-org.github.io/iptv/languages/zho.m3u",
    "英文": "https://iptv-org.github.io/iptv/languages/eng.m3u",
    "印尼语": "https://iptv-org.github.io/iptv/languages/ind.m3u",
    "印地语": "https://iptv-org.github.io/iptv/languages/hin.m3u",
    "@str@1": "https://raw.githubusercontent.com/Broadcasthub/1ptv/refs/heads/main/bhiptv",
}

OUTPUT_DIR = "downloaded_lists"

def download(url, filename):
    try:
        print(f"⬇️ 下载 {filename} 来自 {url}")
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            path = os.path.join(OUTPUT_DIR, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"✅ 保存到 {path}")
        else:
            print(f"⚠️ 下载失败：{url} 状态码 {r.status_code}")
    except Exception as e:
        print(f"❌ 错误：{e}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for lang, url in LANG_URLS.items():
        filename = f"{lang}.m3u"
        download(url, filename)
