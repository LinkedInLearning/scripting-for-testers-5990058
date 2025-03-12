from PIL import Image, ImageDraw

dummy_image = Image.new("RGB", (3000, 2000), (0, 0, 0))
draw = ImageDraw.Draw(dummy_image)
draw.text((10, 10), "600x400", fill=(255, 255, 255))
dummy_image.save("dummy_image.png", quality=100)
