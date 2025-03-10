from playwright.sync_api import Playwright, sync_playwright

base_url = "http://localhost:4001"


def run(playwright: Playwright):
    firefox = playwright.firefox
    browser = firefox.launch(headless=False)
    page = browser.new_page()

    page.goto(f"{base_url}/venues")
    page.screenshot(path="venues_page.png")
    browser.close()

    iphone = playwright.devices["iPhone 15 Pro"]
    webkit = playwright.webkit
    browser = webkit.launch()
    context = browser.new_context(**iphone)

    page = context.new_page()
    page.goto(f"{base_url}/venues")
    page.screenshot(path="venues_page_mobile.png")
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
