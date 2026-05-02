import re, html

with open("favorites_2026_5_2.html", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

stars = []
for line in lines:
    m = re.search(r'javbus\.com/star/([^/"]+)', line)
    if m:
        uid = m.group(1)
        text = line.strip()
        start = text.rfind(">")
        end = text.rfind("</A>")
        if start != -1 and end != -1:
            name = html.unescape(text[start+1:end])
        else:
            name = uid
        name = re.sub(r'\s*-\s*女優.*', '', name)
        name = re.sub(r'\s*-\s*女优.*', '', name)
        name = re.sub(r'\s*-\s*影片.*', '', name)
        stars.append((uid, name.strip()))

yaml_lines = []
yaml_lines.append("settings:")
yaml_lines.append('  proxy: ""')
yaml_lines.append("  batch_size: 20")
yaml_lines.append("  headless: false")
yaml_lines.append("")
yaml_lines.append("stars:")
for uid, name in stars:
    yaml_lines.append(f'  - {{ name: "{name}", id: "{uid}" }}')

with open("config/config.yaml", "w", encoding="utf-8") as f:
    f.write("\n".join(yaml_lines) + "\n")

print(f"共 {len(stars)} 位女优，已写入 config/config.yaml")
