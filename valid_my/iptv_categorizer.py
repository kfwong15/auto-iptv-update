import os
import re
from channel_dict import CHANNEL_OVERRIDES, region_map, type_map, language_from_filename

def match_category(name, mapping, default='其他'):
    for key in mapping:
        if key.lower() in name.lower():
            return mapping[key]
    return default

# 当前目录
base_path = os.path.dirname(__file__)
output_file = os.path.join(base_path, 'iptv_all.m3u')
unclassified_file = os.path.join(base_path, 'unclassified.txt')

output_lines = ['#EXTM3U\n']
unclassified = []

# 遍历所有 *_valid.m3u 文件
for file in os.listdir(base_path):
    if file.endswith('_valid.m3u'):
        language_key = file.replace('_valid.m3u', '')
        language = language_from_filename.get(language_key, '未知语言')

        with open(os.path.join(base_path, file), 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i in range(len(lines)):
            if lines[i].startswith('#EXTINF'):
                extinf = lines[i].strip()
                url = lines[i + 1].strip() if i + 1 < len(lines) else ''

                match = re.search(r',(.+)', extinf)
                channel_name = match.group(1).strip() if match else '未知频道'

                # 优先使用手动覆盖字典
                if channel_name in CHANNEL_OVERRIDES:
                    region, category = CHANNEL_OVERRIDES[channel_name]
                else:
                    region = match_category(channel_name, region_map, '其他地区')
                    category = match_category(channel_name, type_map, '其他')
                    if region == '其他地区' or category == '其他':
                        unclassified.append(f'{language}\t{channel_name}')

                new_extinf = f'#EXTINF:-1 group-title="{language} / {region} / {category}", {channel_name}'
                output_lines.append(new_extinf + '\n')
                output_lines.append(url + '\n')

# 写入 iptv_all.m3u
with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

# 写入未分类频道
with open(unclassified_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(unclassified))

print(f'✅ 生成 {output_file} 成功，共 {len(output_lines)//2} 个频道')
print(f'⚠️ 未分类频道写入 {unclassified_file}，共 {len(unclassified)} 个')
