import os
import sys
import requests
from amazon_paapi import AmazonApi
from amazon_paapi.errors.exceptions import AmazonError, AsinNotFound, AssociateValidationError, InvalidArgument, InvalidPartnerTag, ItemsNotFound, MalformedRequest, RequestError, TooManyRequests
import re
from pprint import pprint as pp
from PIL import Image


def clean_filename(filename):
    # Remove invalid characters for both Windows and Linux
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename)


def add_shadow_to_image(book_cover_path, shadow_path, output_path):
    try:
        with Image.open(book_cover_path) as book_cover:
            with Image.open(shadow_path) as shadow:
                # Calculate new height to maintain aspect ratio
                new_shadow_height = int(
                    shadow.height * (book_cover.width / shadow.width))
                shadow = shadow.resize(
                    (book_cover.width, new_shadow_height), Image.LANCZOS)

                # Create a new image with extra height to accommodate the shadow
                new_height = book_cover.height + shadow.height
                new_image = Image.new('RGBA', (book_cover.width, new_height))

                # Paste the book cover on the new image
                new_image.paste(book_cover, (0, 0))

                # Paste the shadow on the bottom of the new image
                new_image.paste(shadow, (0, book_cover.height), mask=shadow)

                # Save the final image as PNG
                new_image.save(output_path, format='PNG')
                print(f"Image with shadow saved as {output_path}")

                # Delete the original JPEG cover image
                os.remove(book_cover_path)
                print(f"Deleted original book cover image {book_cover_path}")
    except Exception as e:
        print(f"Failed to add shadow to image: {e}")


def get_book_cover_image(url):
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    associate_tag = os.getenv('AWS_ASSOCIATE_TAG')

    if not access_key or not secret_key or not associate_tag:
        print("AWS credentials are not set in environment variables.")
        return

    amazon = AmazonApi(access_key, secret_key, associate_tag, 'BR')

    # Extract the ASIN from the URL
    try:
        asin = url.split('/dp/')[1].split('/')[0]
    except IndexError:
        print("Invalid Amazon URL.")
        return

    try:
        response = amazon.get_items(asin)
        pp(response)

        if response:
            item = response[0]
            if hasattr(item.item_info, 'title'):
                title = item.item_info.title.display_value
                cleaned_title = clean_filename(title)
            else:
                print("Failed to find the title in the response.")
                return

            if hasattr(item.images, 'primary') and hasattr(item.images.primary, 'large'):
                image_url = item.images.primary.large.url

                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    book_cover_path = f"{cleaned_title}.jpg"
                    img_name_with_shadow = f"{cleaned_title}.png"
                    with open(book_cover_path, 'wb') as img_file:
                        img_file.write(img_response.content)
                    print(f"Image saved as {book_cover_path}")

                    # Add shadow to the book cover image
                    shadow_path = os.path.join(
                        os.path.dirname(__file__), 'sombra.png')
                    add_shadow_to_image(
                        book_cover_path, shadow_path, img_name_with_shadow)
                else:
                    print(f"Failed to download the image: {
                          img_response.status_code}")
            else:
                print("Failed to find the book cover image in the response.")
        else:
            print("No items found in the response.")
    except (AmazonError, AsinNotFound, AssociateValidationError, InvalidArgument, InvalidPartnerTag, ItemsNotFound, MalformedRequest, RequestError, TooManyRequests) as e:
        print(f"API response error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <amazon_book_url>")
        sys.exit(1)

    book_url = sys.argv[1]
    get_book_cover_image(book_url)
