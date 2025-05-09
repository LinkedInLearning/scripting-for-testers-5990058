from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright):
    firefox = playwright.firefox
    browser = firefox.launch(headless=False)
    page = browser.new_page()
    url = "http://localhost:4001"

    page.goto(url)
    page.pause()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
