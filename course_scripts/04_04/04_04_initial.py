from playwright.sync_api import Playwright, sync_playwright

base_url = "http://localhost:4001"


def run(playwright: Playwright):
    galaxy = playwright.devices["Galaxy Tab S4 landscape"]
    chromium = playwright.chromium
    browser = chromium.launch()
    context = browser.new_context(**galaxy)

    page = context.new_page()
    page.goto(f"{base_url}/venues")
    page.screenshot(path="venues_page_galaxy.png")
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
