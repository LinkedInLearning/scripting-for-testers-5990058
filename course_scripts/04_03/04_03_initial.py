from playwright.sync_api import Playwright, sync_playwright

base_url = "http://localhost:4001"


def run(playwright: Playwright):
    firefox = playwright.firefox
    browser = firefox.launch(headless=False)
    page = browser.new_page()

    page.goto(f"{base_url}/venues")
    page.screenshot(path="venues_page.png")
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
