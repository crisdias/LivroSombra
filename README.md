# LivroSombra

LivroSombra is a Python script that downloads the cover image of a book from Amazon and adds a shadow to the bottom of the image. The final image is saved in the same directory as the script with the book title as the filename.

## Features

- Downloads the book cover image from Amazon.
- Adds a shadow to the bottom of the cover image.
- Saves the final image as a PNG file.

## Requirements

- Python 3.x
- `requests` library
- `pillow` library
- Amazon Product Advertising API credentials

## Installation

1. Clone the repository:
    git clone https://github.com/crisdias/LivroSombra.git
    cd LivroSombra

2. Create a virtual environment and activate it:
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install the required libraries:
    pip install -r requirements.txt

## Setup

1. Obtain your Amazon Product Advertising API credentials and set them as environment variables:
    export AWS_ACCESS_KEY_ID="your_access_key_id"
    export AWS_SECRET_ACCESS_KEY="your_secret_access_key"
    export AWS_ASSOCIATE_TAG="your_associate_tag"

## Usage

Run the script with the Amazon book URL as a parameter:
    python sombra.py "<amazon_book_url>"

Example:
    python sombra.py "https://www.amazon.com.br/Ensaio-sobre-cancelamento-Pedro-Tourinho/dp/8542226658/"

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
