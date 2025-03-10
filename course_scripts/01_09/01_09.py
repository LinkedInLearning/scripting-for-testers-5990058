import requests

base_url = "http://localhost:4001"

venues = []
for i in range(5):
    capacity = 100 * (i + 1)
    venue_data = {
        "name": f"Venue Capacity: {capacity}",
        "address": "123 main street",
        "city": "Toronto",
        "capacity": capacity,
    }
    venues.append(venue_data)

locations = ["Toronto", "Waterloo", "Kitchener", "Hamilton", "London"]
for location in locations:
    venue_data = {
        "name": f"Venue in: {location}",
        "address": "123 main street",
        "city": location,
        "capacity": 100,
    }
    venues.append(venue_data)

for venue_data in venues:
    response = requests.post(url=f"{base_url}/api/venues", json=venue_data)
    print(response.status_code)
