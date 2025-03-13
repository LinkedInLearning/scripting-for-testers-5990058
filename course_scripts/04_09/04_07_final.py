from PIL import Image, ImageChops, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

base_url = "https://redesigned-space-funicular-wq474pxq9jf57xw-8000.app.github.dev"


def compare_images(image1, image2):
    img1 = Image.open(image1).convert("RGB")
    img2 = Image.open(image2).convert("RGB")
    diff = ImageChops.difference(img1, img2)
    diff.save(f"diff_{image1}_{image2}.png")

    max_height = max(img1.height, img2.height)
    label_height = 80
    combined = Image.new("RGB", (img1.width + img2.width, max_height + label_height))
    combined.paste(img1, (0, label_height))
    combined.paste(img2, (img1.width, label_height))

    font = ImageFont.load_default(size=42)
    draw = ImageDraw.Draw(combined)
    draw.text((0, 0), image1, font=font)
    draw.text((img1.width, 0), image2, font=font)

    combined.save(f"combined_{image1}_{image2}.png")

    if diff.getbbox():
        print("Images are different")
    else:
        print("Images are the same")


def run(browser_type):
    browser = browser_type.launch(headless=False)

    page = browser.new_page()
    page.goto(f"{base_url}/venues")
    page.get_by_role("button", name="Continue", exact=True).click()
    screenshot_path = f"venues_page_{browser_type.name}.png"
    page.screenshot(path=screenshot_path)
    browser.close()

    return screenshot_path


with sync_playwright() as playwright:
    screenshots = []
    for browser_type in [playwright.chromium, playwright.firefox, playwright.webkit]:
        screenshot_path = run(browser_type)
        screenshots.append(screenshot_path)
    for index, screenshot in enumerate(screenshots):
        for remaining_screenshot in screenshots[index + 1 :]:
            compare_images(screenshot, remaining_screenshot)
