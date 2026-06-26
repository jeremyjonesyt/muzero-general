from playwright.sync_api import sync_playwright

class WebAgent:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def perform_action(self, url, selector):
        self.page.goto(url)
        self.page.click(selector)
        return self.page.content()  # This 'content' is your next-state signal

    def close(self):
        self.browser.close()
        self.playwright.stop()
