import requests
from bs4 import BeautifulSoup

base_url = "http://localhost:4001"


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


response = requests.get(f"{base_url}/gigs")
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table")

future_table_data = parse_data_from_table(table)
print(future_table_data)
