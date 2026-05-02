import webbrowser

from src.utils.logger import log_info, log_success, log_warning


def open_batch(urls, batch_size):
    if not urls:
        log_warning("没有需要打开的链接")
        return

    total = len(urls)
    log_info(f"共 {total} 个链接，每批 {batch_size} 个")

    opened = 0
    while opened < total:
        chunk = urls[opened:opened + batch_size]

        for url in chunk:
            webbrowser.open(url)

        opened += len(chunk)
        log_success(f"已打开 {opened}/{total}")

        if opened >= total:
            break

        answer = input(f"\n输入 'y' 继续下一批，其他键退出: ").strip().lower()
        if answer != "y":
            log_warning(f"已退出，共打开 {opened}/{total} 个链接")
            return

    log_success(f"全部 {total} 个链接已处理完毕")
