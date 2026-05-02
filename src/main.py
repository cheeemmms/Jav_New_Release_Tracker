import sys
from datetime import date

from src.utils.config_loader import load_yaml, load_json, save_json
from src.utils.logger import log_title, log_info, log_success, log_warning, log_error, ask_choice, ask_date
from src.scraper.engine import BrowserEngine, random_delay
from src.scraper.parser import parse_star_page
from src.output.md_generator import generate_report
from src.output.browser_opener import open_batch


def main():
    log_title("JAV New Release Tracker")

    log_info("加载配置...")
    config = load_yaml("config/config.yaml")
    stars = config.get("stars", [])
    settings = config.get("settings", {})

    if not stars:
        log_error("未配置任何女优，请编辑 config/config.yaml")
        sys.exit(1)

    last_run = load_json("config/state.json", default={}).get("last_run_date", "")

    cutoff_date = last_run
    if last_run:
        choice = ask_choice(
            f"上次运行日期: {last_run}，请选择:",
            [f"使用上次日期 ({last_run})", "手动输入新日期"]
        )
        if choice == 2:
            cutoff_date = ask_date("请输入起始日期")
    else:
        log_info("首次运行，请输入起始日期")
        cutoff_date = ask_date("请输入起始日期")

    log_info(f"目标起始日期: {cutoff_date}")

    all_results = {}
    total_new = 0

    log_title("开始抓取")

    with BrowserEngine(config) as engine:
        for idx, star in enumerate(stars, 1):
            name = star.get("name", "未知")
            uid = star.get("id", "")
            if not uid:
                log_warning(f"[{idx}/{len(stars)}] {name}: 缺少 ID，跳过")
                all_results[name] = []
                continue

            url = f"https://www.javbus.com/star/{uid}"
            log_info(f"[{idx}/{len(stars)}] 正在抓取: {name} ({uid})")

            try:
                if idx > 1:
                    random_delay(3, 7)

                soup = engine.navigate(url)
                movies = parse_star_page(soup, name, cutoff_date)
                all_results[name] = movies

                if movies:
                    log_success(f"  {name}: 发现 {len(movies)} 部新作品")
                    total_new += len(movies)
                else:
                    log_info(f"  {name}: 暂无新作品")
            except Exception as e:
                log_error(f"  {name}: 抓取失败 - {e}")
                all_results[name] = []

    log_title("生成报告")

    batch_size = settings.get("batch_size", 20)
    report_path = generate_report(all_results, "outputs")

    if total_new > 0:
        all_urls = []
        for movies in all_results.values():
            for m in movies:
                all_urls.append(m.get("url", ""))

        if all_urls:
            open_batch(all_urls, batch_size)
    else:
        log_info("没有新作品，跳过浏览器预览")

    today = date.today().strftime("%Y-%m-%d")
    save_json("config/state.json", {"last_run_date": today})
    log_success(f"状态已更新: last_run_date = {today}")

    log_success("所有任务完成!")


if __name__ == "__main__":
    main()
