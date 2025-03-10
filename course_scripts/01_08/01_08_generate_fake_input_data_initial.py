import requests

base_url = "http://localhost:4001"

for _ in range(5):
    response = requests.post(
        f"{base_url}/api/gigs",
        json={
            "venue": "Test Venue",
            "date": "2022-01-01",
            "time": "12:00",
        },
    )
    print(f"Created gig: {response.json()}")
