from playwright.sync_api import Page, Playwright, sync_playwright


def create_gig_and_search(page: Page, gig_name: str):
    page.get_by_role("button", name="Add a Gig").click()
    page.get_by_placeholder("Enter gig name").click()
    page.get_by_placeholder("Enter gig name").fill(gig_name)
    page.get_by_label("Gig Date").fill("2025-01-22")
    page.get_by_role("button", name="Submit").click()

    page.locator(".bi").first.click()
    page.get_by_placeholder("Search").click()
    page.get_by_placeholder("Search").fill(gig_name)
    page.keyboard.press("Enter")


def run(playwright: Playwright):
    firefox = playwright.firefox
    browser = firefox.launch(headless=False)
    page = browser.new_page()
    url = "http://localhost:4001"

    page.goto(url)

    gig_names = ["Test", "Temp", "!@#$%^&*()"]
    for gig_name in gig_names:
        create_gig_and_search(page, gig_name)
        page.pause()
        page.goto(url)

    browser.close()


with sync_playwright() as playwright:
    run(playwright)
