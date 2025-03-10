import requests
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, expect, sync_playwright

base_url = "http://localhost:4001/gigs"

response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")


def parse_data_from_table(table):
    headers = []
    for header in table.find_all("th"):
        headers.append(header.text.strip())

    results_dict = {header: [] for header in headers}
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        for index, cell in enumerate(cells):
            results_dict[headers[index]].append(cell.text)

    return results_dict


table = soup.find("table")

table_data = parse_data_from_table(table)
print(table_data)


def run(playwright: Playwright):
    firefox = playwright.firefox
    browser = firefox.launch(headless=False)
    page = browser.new_page()

    page.goto(base_url)
    page.locator("#gig-date-filter").select_option("past")

    expect(page.locator("td").first).to_be_visible()

    content = page.content()
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table")
    table_data = parse_data_from_table(table)

    print(table_data)

    page.pause()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
