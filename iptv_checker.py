# iptv_checker.py

import os
import requests
from tqdm import tqdm

INPUT_DIR = "downloaded_lists"
OUTPUT_DIR = "valid_my"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def is_stream_alive(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=5, stream=True)
        return r.status_code == 200
    except Exception:
        return False

def filter_valid_streams(input_file, output_file):
    valid_lines = []
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i in tqdm(range(0, len(lines))):
        line = lines[i].strip()
        if line.startswith("http"):
            extinf = lines[i - 1].strip() if i > 0 else "#EXTINF:-1"
            if is_stream_alive(line):
                valid_lines.append(extinf + "\n" + line + "\n")

    if valid_lines:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for entry in valid_lines:
                f.write(entry)
        print(f"[✓] 保存 {len(valid_lines)} 个可播放频道 -> {output_file}")
    else:
        print(f"[✘] 无有效频道 -> {output_file} 未创建")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for file in os.listdir(INPUT_DIR):
        if file.endswith(".m3u"):
            lang = file.replace(".m3u", "")
            input_path = os.path.join(INPUT_DIR, file)
            output_path = os.path.join(OUTPUT_DIR, f"{lang}_valid.m3u")
            filter_valid_streams(input_path, output_path)
