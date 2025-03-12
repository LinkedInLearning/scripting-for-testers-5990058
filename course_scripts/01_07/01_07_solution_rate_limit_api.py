import requests

base_url = "http://localhost:4001"

session = requests.Session()

for _ in range(10):
    response = session.post(
        f"{base_url}/api/gigs",
        json={
            "venue_id": 0,
            "client_id": 1,
            "name": "Test Gig",
            "date": "2025-01-01",
            "time": "12:00",
        },
    )
    print(f"Created gig: {response.status_code}")

    try:
        gig_id = response.json()["id"]
    except KeyError:
        continue
    response = session.delete(f"{base_url}/api/gigs/{gig_id}")
    print(f"Deleted Gig: {response.status_code}")

for _ in range(5):
    response = session.get(f"{base_url}/api/gigs")
    # time.sleep(1)
    print(f"Get gigs: {response.status_code}")


for _ in range(15):
    response = session.put(
        f"{base_url}/api/gigs/{gig_id}",
        json={
            "venue_id": 0,
            "client_id": 1,
            "name": "Updated Gig",
            "date": "2025-01-01",
            "time": "12:00",
        },
    )
    print(f"Updated gig: {response.status_code}")
