from playwright.sync_api import Page, Playwright, sync_playwright


def open_gig_form(page: Page):
    page.get_by_role("button", name="Add a Gig").click()


def add_venue(page: Page):
    page.get_by_label("Venue").select_option("/venues")
    page.goto("http://localhost:4001/venues")
    page.get_by_role("button", name="Add a Venue").click()
    page.get_by_placeholder("Enter the Venue name").click()
    page.get_by_placeholder("Enter the Venue name").fill("Golf Course")
    page.get_by_placeholder("Enter the Venue name").press("Tab")
    page.get_by_label("Adress").fill("123 Main street")
    page.get_by_label("Adress").press("Tab")
    page.get_by_label("City", exact=True).fill("Somewhere")
    page.get_by_label("City", exact=True).press("Tab")
    page.get_by_label("Contact Number").fill("123-123-1234")
    page.get_by_label("Contact Number").press("Tab")
    page.get_by_label("Contact Email Address").fill("test@test.com")
    page.get_by_label("Contact Email Address").press("Tab")
    page.get_by_label("Venue Capacity").fill("100")
    page.get_by_label("Venue Capacity").press("Tab")
    page.get_by_label("Notes").fill("Cool place")
    page.get_by_role("button", name="Submit").click()


def add_client(page: Page):
    page.get_by_label("Client").select_option("/clients")
    page.goto("http://localhost:4001/clients")
    page.get_by_role("button", name="Add a Client").click()
    page.get_by_placeholder("Enter the Client's first name").click()
    page.get_by_placeholder("Enter the Client's first name").fill("David")
    page.get_by_placeholder("Enter the Client's first name").press("Tab")
    page.get_by_placeholder("Enter the Client's last name").fill("Westerveld")
    page.get_by_placeholder("Enter the Client's last name").press("Tab")
    page.locator("#client-address").fill("987 Second Ave")
    page.locator("#client-address").press("Tab")
    page.locator("#client-city").fill("Pleansantville")
    page.locator("#client-city").press("Tab")
    page.locator("#client-contact_number").fill("987-987-0987")
    page.locator("#client-contact_number").press("Tab")
    page.locator("#client-contact_email").fill("test2@test.com")
    page.get_by_role("button", name="Submit").click()


def add_gig(page: Page):
    page.get_by_role("button", name="Add a Gig").click()
    page.get_by_label("Venue").select_option("1")
    page.get_by_label("Client").select_option("1")
    page.get_by_placeholder("Enter gig name").click()
    page.get_by_placeholder("Enter gig name").fill("Gig Test")
    page.get_by_label("Gig Date").fill("2025-01-30")
    page.get_by_role("button", name="Submit").click()


def run(playwright: Playwright):
    firefox = playwright.firefox
    browser = firefox.launch(headless=False)
    page = browser.new_page()
    url = "http://localhost:4001"

    page.goto(url)

    open_gig_form(page)

    # Scenario 1: Create a gig with a new client and a new venue
    add_venue(page)

    page.get_by_role("link", name=" Home").click()
    page.get_by_role("button", name="Add a Gig").click()

    add_client(page)

    page.get_by_role("link", name=" Home").nth(1).click()

    add_gig(page)

    page.pause()

    # Scenario 2: Create a gig with a new client, but at a previously used venue
    page.goto(url)

    open_gig_form(page)
    add_client(page)

    page.get_by_role("link", name=" Home").nth(1).click()

    add_gig(page)
    page.pause()

    # Scenario 3: Create a gig for both a client and location that we worked with before
    page.goto(url)

    add_gig(page)
    page.pause()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
