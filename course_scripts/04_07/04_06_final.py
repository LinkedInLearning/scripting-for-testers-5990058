from PIL import Image, ImageDraw

# Generate a dummy image
dummy_image = Image.new("RGB", (600, 400), (0, 0, 0))
draw = ImageDraw.Draw(dummy_image)
draw.text((10, 10), "600x400", fill=(255, 255, 255))

cropped_image = dummy_image.crop((0, 0, 100, 25))
cropped_image.save("cropped_image.png")


# Check if the cropped image is a sub image in the original image
def is_sub_image(cropped, original):
    cropped_data = list(cropped.getdata())
    for y in range(original.height - cropped.height + 1):
        for x in range(original.width - cropped.width + 1):
            box = (x, y, x + cropped.width, y + cropped.height)
            region = original.crop(box)
            if list(region.getdata()) == cropped_data:
                return True
    return False


if is_sub_image(cropped_image, dummy_image):
    print("Cropped image is in the original image")

dummy_image2 = Image.new("RGB", (600, 400), (0, 0, 0))
draw = ImageDraw.Draw(dummy_image)
draw.text((10, 10), "Different Text", fill=(255, 255, 255))

if is_sub_image(cropped_image, dummy_image2):
    print("Cropped image is in the original image")
else:
    print("Cropped image is not in the original image")
