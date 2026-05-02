import os
from datetime import date

from src.utils.logger import log_success, log_info


def generate_report(results, output_dir):
    today = date.today().strftime("%Y%m%d")
    filename = f"Updates_{today}.md"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    lines = []
    lines.append(f"# JAV 更新报告 ({date.today().strftime('%Y-%m-%d')})")
    lines.append("")

    total_movies = 0

    for star_name, movies in results.items():
        lines.append(f"## {star_name}")
        lines.append("")

        if not movies:
            lines.append("> 暂无更新")
            lines.append("")
            continue

        for idx, m in enumerate(movies, 1):
            title = m.get("title", "未知标题")
            url = m.get("url", "")
            movie_date = m.get("date", "")
            lines.append(f"{idx}. **{title}**")
            lines.append(f"   - 日期: {movie_date}")
            lines.append(f"   - 链接: [{url}]({url})")
            lines.append("")
            total_movies += 1

    lines.append("---")
    lines.append(f"*共 {total_movies} 部新作品，{len(results)} 位女优*")

    content = "\n".join(lines)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    log_success(f"报告已生成: {filepath}")
    log_info(f"共 {total_movies} 部新作品")
    return filepath
