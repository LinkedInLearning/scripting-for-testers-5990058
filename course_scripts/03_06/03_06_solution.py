from datetime import datetime

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


def validate_gig_data(gig_data, future=True):
    dates = gig_data["Date"]
    for date in dates:
        gig_date = datetime.strptime(date, "%Y-%m-%d")
        if future:
            assert gig_date > datetime.now(), f"Found a past gig: {date}"
        else:
            assert gig_date < datetime.now(), f"Found a future gig: {date}"


response = requests.get(f"{base_url}/api/venues")
venues = response.json()
venue_id = venues[0]["id"]


data = {"username": "user1", "password": "password"}
response = requests.post(f"{base_url}/token", data=data)
token_dict = response.json()

header = {"Authorization": "Bearer " + token_dict["access_token"]}
response = requests.get(f"{base_url}/api/clients", headers=header)
clients = response.json()
client_id = clients[0]["id"]

response = requests.post(
    f"{base_url}/api/gigs",
    json={
        "name": "Future gig",
        "venue_id": venue_id,
        "date": "2030-01-01",
        "time": "12:00",
        "client_id": client_id,
    },
)
print(response.json())
response = requests.get(f"{base_url}/gigs")
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table")

future_table_data = parse_data_from_table(table)
print(future_table_data)
validate_gig_data(future_table_data)

response = requests.get(f"{base_url}/filter_gigs?filter=past")
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table")

past_table_data = parse_data_from_table(table)
print(past_table_data)
validate_gig_data(past_table_data, future=False)
