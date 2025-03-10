import faker
import requests

fake = faker.Faker()

base_url = "http://localhost:4001"

for _ in range(5):
    response = requests.post(
        f"{base_url}/api/gigs",
        json={
            "venue": fake.text(max_nb_chars=20),
            "date": fake.date(),
            "time": fake.time(pattern="%H:%M"),
        },
    )
    print(f"Created gig: {response.json()}")
