# iptv_checker.py

import os
import requests
import subprocess
from tqdm import tqdm

INPUT_FILE = "iptv_all.m3u"
OUTPUT_DIR = "valid_my"

def check_http_ok(url):
    try:
        r = requests.get(url, timeout=5)
        return r.status_code == 200
    except:
        return False

def check_ffmpeg_playable(url):
    try:
        result = subprocess.run(
            ["ffmpeg", "-loglevel", "error", "-i", url, "-t", "3", "-f", "null", "-"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )
        return b"frame=" in result.stderr or b"Video" in result.stderr
    except:
        return False

def classify(name_line):
    lang, region = "未知语言", "未知地区"
    if "tvg-language=" in name_line:
        if "zh" in name_line:
            lang = "中文"
        elif "en" in name_line:
            lang = "英文"
        elif "id" in name_line:
            lang = "印尼语"
        elif "hi" in name_line:
            lang = "印地语"
    if "tvg-country=" in name_line:
        if "CN" in name_line:
            region = "中国大陆"
        elif "HK" in name_line:
            region = "香港"
        elif "TW" in name_line:
            region = "台湾"
        elif "MY" in name_line:
            region = "马来西亚"
        elif "ID" in name_line:
            region = "印尼"
        elif "IN" in name_line:
            region = "印度"
        elif "SG" in name_line:
            region = "新加坡"
        elif "US" in name_line:
            region = "美国"
        elif "GB" in name_line:
            region = "英国"
    return lang, region

def save_stream(lang, region, name, url):
    folder = os.path.join(OUTPUT_DIR, lang, region)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "channels.m3u")
    with open(path, "a", encoding="utf-8") as f:
        f.write(name + "\n" + url + "\n")

def process_all():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total = 0
    for i in tqdm(range(len(lines))):
        if lines[i].startswith("#EXTINF"):
            name = lines[i].strip()
            url = lines[i+1].strip() if i+1 < len(lines) else ""
            if url.startswith("http"):
                if check_http_ok(url):
                    if check_ffmpeg_playable(url):
                        lang, region = classify(name)
                        save_stream(lang, region, name, url)
                        total += 1
    print(f"[✓] 完成，保存 {total} 个可播放频道")

if __name__ == "__main__":
    process_all()
