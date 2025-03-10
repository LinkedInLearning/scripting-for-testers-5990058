import requests
from bs4 import BeautifulSoup

base_url = "http://localhost:4001"

response = requests.get(base_url)

soup = BeautifulSoup(response.text, "html.parser")

nav = soup.find("div", class_="sidebar")

nav_links = nav.find_all("a")

for link in nav_links:
    href = link.get("href")
    url = f"{base_url}{href}"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if not table:
        continue

    headers = []
    for header in table.find_all("th"):
        headers.append(header.text.strip())

    results_dict = {header: [] for header in headers}
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        for index, cell in enumerate(cells):
            results_dict[headers[index]].append(cell.text)
    print(results_dict)
