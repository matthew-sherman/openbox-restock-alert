import os

import requests
from dotenv import load_dotenv

# Load environment variables from .env into system memory
load_dotenv()

# Get product url from system memory
PRODUCT_URL = os.environ.get("PRODUCT_URL")


def fetch_html(url):
    # Use a desktop User-Agent to prevent anti-bot blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    return response.text


def check_stock_status():
    html = fetch_html(PRODUCT_URL)
    return
