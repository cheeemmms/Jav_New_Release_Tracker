import random
import time
import os

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def random_delay(min_s=3, max_s=7):
    time.sleep(random.uniform(min_s, max_s))


def _find_system_browser():
    if os.name != "nt":
        return None
    candidates = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
        "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


class BrowserEngine:
    def __init__(self, config):
        settings = config.get("settings", {})
        self._proxy = settings.get("proxy", "")
        self._headless = settings.get("headless", False)
        self._playwright = None
        self._browser = None
        self._page = None

    def start(self):
        self.close()

        self._playwright = sync_playwright().start()

        if self._proxy:
            launch_options = {"proxy": {"server": self._proxy}}
        else:
            launch_options = {}

        launch_options["headless"] = self._headless

        browser_launched = False

        system_browser = _find_system_browser()
        if system_browser:
            try:
                launch_options["executable_path"] = system_browser
                self._browser = self._playwright.chromium.launch(**launch_options)
                browser_launched = True
            except Exception:
                launch_options.pop("executable_path", None)
                launch_options.pop("proxy", None)

        if not browser_launched:
            launch_options.pop("executable_path", None)
            try:
                self._browser = self._playwright.chromium.launch(**launch_options)
                browser_launched = True
            except Exception:
                pass

        if not browser_launched:
            raise RuntimeError(
                "浏览器启动失败。请确认：\n"
                "1. Chrome 或 Edge 已安装\n"
                "2. 或者执行: playwright install chromium"
            )

        context = self._browser.new_context()

        try:
            from playwright_stealth import StealthConfig, stealth_sync
            stealth_sync(context, StealthConfig(navigator_languages=False))
        except Exception:
            pass

        self._page = context.new_page()
        self._page.set_default_timeout(30000)

    def navigate(self, url, timeout=30000):
        self._page.set_default_timeout(timeout)
        self._page.goto(url, wait_until="domcontentloaded")
        content = self._page.content()
        return BeautifulSoup(content, "html.parser")

    def close(self):
        try:
            if self._browser:
                self._browser.close()
        except Exception:
            pass
        try:
            if self._playwright:
                self._playwright.stop()
        except Exception:
            pass

    def is_alive(self):
        try:
            if self._browser and self._page:
                self._page.evaluate("1 + 1")
                return True
        except Exception:
            pass
        return False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.close()
