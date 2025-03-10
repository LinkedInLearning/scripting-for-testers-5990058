import requests

base_url = "http://localhost:4001"

for _ in range(10):
    response = requests.post(
        f"{base_url}/api/gigs",
        json={
            "venue": "Test Venue",
            "date": "2022-01-01",
            "time": "12:00",
        },
    )
    print(f"Created gig: {response.status_code}")

    try:
        gig_id = response.json()["id"]
    except KeyError:
        continue
    response = requests.delete(f"{base_url}/api/gigs/{gig_id}")
    print(f"Deleted Gig: {response.status_code}")

for _ in range(5):
    response = requests.get(f"{base_url}/api/gigs")
    # time.sleep(1)
    print(f"Get gigs: {response.status_code}")


for _ in range(15):
    response = requests.put(
        f"{base_url}/api/gigs/{gig_id}",
        json={
            "venue": "Updated Venue",
            "date": "2022-01-01",
            "time": "12:00",
        },
    )
    print(f"Updated gig: {response.status_code}")
