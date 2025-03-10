from PIL import Image, ImageChops, ImageDraw, ImageFont
from playwright.sync_api import Playwright, sync_playwright

base_url = "http://localhost:4001"


def compare_images(image1, image2):
    img1 = Image.open(image1).convert("RGB")
    img2 = Image.open(image2).convert("RGB")
    diff = ImageChops.difference(img1, img2)
    diff.save("diff.png")

    max_height = max(img1.height, img2.height)
    label_height = 80
    combined = Image.new("RGB", (img1.width + img2.width, max_height + label_height))
    combined.paste(img1, (0, label_height))
    combined.paste(img2, (img1.width, label_height))

    font = ImageFont.load_default(size=42)
    draw = ImageDraw.Draw(combined)
    draw.text((0, 0), image1, font=font)
    draw.text((img1.width, 0), image2, font=font)

    combined.save("combined.png")

    if diff.getbbox():
        print("Images are different")
    else:
        print("Images are the same")


def run(playwright: Playwright):
    file_paths = []
    for device in ["Galaxy Tab S4 landscape", "iPad Pro 11 landscape"]:
        current_device = playwright.devices[device]
        chromium = playwright.chromium
        browser = chromium.launch()
        context = browser.new_context(**current_device)

        page = context.new_page()
        page.goto(f"{base_url}/venues")
        screenshot_path = f"venues_page_{device.replace(' ', '_')}.png"
        file_paths.append(screenshot_path)
        page.screenshot(path=screenshot_path)
        browser.close()

    compare_images(file_paths[0], file_paths[1])


with sync_playwright() as playwright:
    run(playwright)
