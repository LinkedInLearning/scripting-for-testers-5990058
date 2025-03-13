from PIL import Image, ImageDraw

# Generate a dummy image
dummy_image = Image.new("RGB", (3000, 2000), (0, 0, 0))
draw = ImageDraw.Draw(dummy_image)
draw.text((10, 10), "600x400", fill=(255, 255, 255))
