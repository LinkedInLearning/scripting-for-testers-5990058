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
    print(response.text)
