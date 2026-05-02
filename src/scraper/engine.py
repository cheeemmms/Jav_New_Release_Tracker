import random
import time

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def random_delay(min_s=3, max_s=7):
    time.sleep(random.uniform(min_s, max_s))


class BrowserEngine:
    def __init__(self, config):
        settings = config.get("settings", {})
        self._proxy = settings.get("proxy", "")
        self._headless = settings.get("headless", False)
        self._playwright = None
        self._browser = None
        self._page = None

    def start(self):
        self._playwright = sync_playwright().start()
        launch_options = {"headless": self._headless}

        if self._proxy:
            launch_options["proxy"] = {"server": self._proxy}

        try:
            self._browser = self._playwright.chromium.launch(**launch_options)
        except Exception:
            self._browser = self._playwright.chromium.launch(headless=self._headless)

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
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.close()
