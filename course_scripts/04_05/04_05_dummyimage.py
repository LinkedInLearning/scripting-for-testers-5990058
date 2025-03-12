import requests

img_dimensions = "600x400"
response = requests.get(f"https://dummyimage.com/{img_dimensions}/000/fff")

with open("image.png", "wb") as file:
    file.write(response.content)
