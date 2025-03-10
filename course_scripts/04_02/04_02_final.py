import requests
from PIL import Image, ImageChops
from playwright.sync_api import Playwright, sync_playwright

base_url = "http://localhost:4001"


def run(playwright: Playwright):
    firefox = playwright.firefox
    browser = firefox.launch(headless=False)
    page = browser.new_page()

    page.goto(f"{base_url}/venues")
    page.screenshot(path="venues_page.png")
    browser.close()


def create_venue():
    venue_data = {
        "name": "Test Venue",
        "address": "123 Main St",
        "city": "Springfield",
        "contact_number": "555-555-5555",
        "contact_email": "test@test.com",
        "capacity": 100,
        "notes": "Great venue!",
    }
    requests.post(f"{base_url}/api/venues", json=venue_data)


def compare_images(image1, image2):
    img1 = Image.open(image1).convert("RGB")
    img2 = Image.open(image2).convert("RGB")
    diff = ImageChops.difference(img1, img2)
    diff.save("diff.png")

    if diff.getbbox():
        print("Images are different")
    else:
        print("Images are the same")


create_venue()
with sync_playwright() as playwright:
    run(playwright)

compare_images("venues_page.png", "venues_page_baseline.png")
