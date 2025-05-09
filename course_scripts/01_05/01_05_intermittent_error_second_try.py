import requests

base_url = "<put your url in here>"


# In the video, we added in authorization and then
# tried again as can be seen in the code below
token_data = {"username": "user1", "password": "password"}
response = requests.post(f"{base_url}/token", data=token_data)
token = response.json()["access_token"]

headers = {"Authorization": f"Bearer {token}"}

data = {
    "email_address": "fake@fake.com",
    "first_name": "Dave",
    "last_name": "Westerveld",
    "phone_number": "1-519-123-4567",
    "address": "24 Fake St",
    "city": "Brantford",
    "province": "Ontario",
    "zip": "N3R 1A1",
    "country": "Canada",
}


response = requests.post(f"{base_url}/api/clients", json=data, headers=headers)
client_id = response.json()["id"]

response = requests.get(f"{base_url}/api/clients/{client_id}", headers=headers)
print(response.json())
