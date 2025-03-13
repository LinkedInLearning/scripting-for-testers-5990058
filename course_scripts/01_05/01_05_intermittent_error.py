import requests

base_url = "http://localhost:4001"

# TODO: Add permanent user to DB
data = {
    "username": "user1",
    "first_name": "Dave",
    "last_name": "Westerveld",
    "email_address": "fake@fake.com",
    "password": "password",
}
requests.post(f"{base_url}/api/users", json=data)


#


def first_try():
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


def second_try():
    data = {"username": "user1", "password": "password"}
    response = requests.post(f"{base_url}/token", data=data)
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

    for _ in range(10):
        response = requests.post(f"{base_url}/api/clients", json=data, headers=headers)
        client_id = response.json()["id"]

        response = requests.get(f"{base_url}/api/clients/{client_id}", headers=headers)
        print(response.json())


# try:
#     first_try()
# except KeyError as e:
#     assert e.args[0] == "id"

second_try()
