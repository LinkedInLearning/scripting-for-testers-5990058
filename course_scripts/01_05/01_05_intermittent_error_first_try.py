import requests

base_url = "<put your url in here>"

# In the video, we first ran this code and 
# get an error about not being able to find the client id
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

response = requests.post(f"{base_url}/api/clients", json=data)

client_id = response.json()["id"]

response = requests.get(f"{base_url}/api/clients/{client_id}")
print(response.json())
