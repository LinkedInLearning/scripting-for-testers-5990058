import requests
from bs4 import BeautifulSoup

base_url = "http://localhost:4001"

response = requests.get(f"{base_url}/venues")

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
parsed_data = parse_data_from_table(table)

print(parsed_data)
