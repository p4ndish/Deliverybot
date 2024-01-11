from PIL import Image
import requests
from io import BytesIO

def combine_images_from_urls(image_urls):
    images = []
    output_file = "bot/../web_service/images/logo/checkout_cart.jpg"
    # Download images from URLs
    for url in image_urls:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        images.append(img)

    width, height = images[0].size

    combined_image = Image.new('RGB', (width, height * len(images)))

    for i, img in enumerate(images):
        combined_image.paste(img, (0, i * height))

    combined_image.save(output_file)
    img = Image.open(output_file)
    width, height = img.size
    return height, width



def get_image_size(image_path):
    # Open the image file
    img = Image.open(image_path)
    width, height = img.size
    print(f"Image Size: {width} x {height}")

# image_urls = [
    
#     "https://f8ce-196-191-61-125.ngrok-free.app/images/angla/burger-Medium-Cheese-HAM-EGG-Burger-Large.png",
#     "https://f8ce-196-191-61-125.ngrok-free.app/images/angla/burger-Large-ANGLA-SPECIAL.png",
#     "https://f8ce-196-191-61-125.ngrok-free.app/images/angla/burger-Large-ANGLA-SPECIAL.png",
# ]

# combine_images_from_urls(image_urls, output_file)

