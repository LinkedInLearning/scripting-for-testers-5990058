from playwright.sync_api import Page, Playwright, sync_playwright


def open_gig_form(page: Page):
    page.get_by_role("button", name="Add a Gig").click()


def run(playwright: Playwright):
    firefox = playwright.firefox
    browser = firefox.launch(headless=False)
    page = browser.new_page()
    url = "http://localhost:4001"

    page.goto(url)

    open_gig_form(page)

    page.pause()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
