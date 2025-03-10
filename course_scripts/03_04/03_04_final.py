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


# create a new venue
# name = parsed_data["Name"][0]
# address = parsed_data["Address"][0]
# phone_number = parsed_data["Phone Number"][0]
# email = parsed_data["Email Address"][0]
# response = requests.post(
#     f"{base_url}/api/venues",
#     json={
#         "name": name,
#         "address": address,
#         "contact_number": phone_number,
#         "contact_email": email,
#     },
# )

# response = requests.get(f"{base_url}/venues")

# soup = BeautifulSoup(response.text, "html.parser")
# table = soup.find("table")
# parsed_data = parse_data_from_table(table)

for key, item in parsed_data.items():
    seen = set()
    for value in item:
        if value in seen:
            print(
                f"Found a potential duplicate. The key '{key}' contains this value twice: {value}"
            )
        seen.add(value)
