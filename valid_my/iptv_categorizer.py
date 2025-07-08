import os import re

def match_category(name, mapping, default='其他'): for key in mapping: if key.lower() in name.lower(): return mapping[key] return default

====== 分类关键词字典 ======

language_from_filename = { '中文': '中文', '英文': '英文', '印地语': '印地语', '印尼语': '印尼语' }

region_map = { 'CCTV': '中国大陆', 'CGTN': '中国大陆', '凤凰': '香港', 'TVB': '香港', '中天': '台湾', '东森': '台湾', 'Astro': '马来西亚', '新传媒': '新加坡', 'Channel 8': '新加坡', 'BBC': '英国', 'CNN': '美国', 'HBO': '美国', 'ESPN': '美国', 'ABC': '澳大利亚', 'Zee': '印度', 'Star': '印度', 'Trans': '印尼', 'RCTI': '印尼', 'TVRI': '印尼', 'Metro': '印尼' }

type_map = { '新闻': '新闻', 'News': '新闻', 'CCTV-13': '新闻', 'BBC': '新闻', 'CNN': '新闻', '娱乐': '娱乐', '综艺': '娱乐', 'Star': '娱乐', 'TVB': '娱乐', 'Astro': '娱乐', 'Trans': '娱乐', '电影': '电影', 'Cinema': '电影', 'HBO': '电影', '体育': '体育', 'Sports': '体育', 'ESPN': '体育', '儿童': '儿童', 'Kids': '儿童', 'Cartoon': '儿童', '音乐': '音乐', 'Music': '音乐', '宗教': '宗教', 'TVRI': '宗教', '教育': '教育', 'Education': '教育' }

base_path = os.path.dirname(file) output_file = os.path.join(base_path, 'iptv_all.m3u')

output_lines = ['#EXTM3U\n']

遍历 valid_my 目录下的所有 *_valid.m3u 文件

for file in os.listdir(base_path): if file.endswith('_valid.m3u'): language_key = file.replace('_valid.m3u', '') language = language_from_filename.get(language_key, '未知语言')

with open(os.path.join(base_path, file), 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        if lines[i].startswith('#EXTINF'):
            extinf = lines[i].strip()
            url = lines[i + 1].strip() if i + 1 < len(lines) else ''

            match = re.search(r',(.+)', extinf)
            channel_name = match.group(1).strip() if match else '未知频道'

            region = match_category(channel_name, region_map, '其他地区')
            category = match_category(channel_name, type_map, '其他')

            new_extinf = f'#EXTINF:-1 group-title="{language} / {region} / {category}", {channel_name}'
            output_lines.append(new_extinf + '\n')
            output_lines.append(url + '\n')

with open(output_file, 'w', encoding='utf-8') as f: f.writelines(output_lines)

print(f'✅ 成功生成：{output_file}，共 {len(output_lines)//2} 个频道')
