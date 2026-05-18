import os
import re

import requests
from bs4 import BeautifulSoup
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


def parse_html(html):
    return BeautifulSoup(html, "html.parser")


def extract_product_data(soup):
    product = {
        "name": "",
        "model_number": "",
        "color": "",
        "capacity": "",
        "available": False,
    }

    title_el = soup.select_one(".product-meta__title")
    if title_el:
        title = title_el.get_text(strip=True)
        match = re.search(r"(Apple\s+.*?)(?:\s+Unlocked|\s+-|$)", title)
        if match:
            product["name"] = match.group(1).strip()
        else:
            product["name"] = title.split("-")[0].strip()

    sku_el = soup.select_one(".product-meta__sku-number")
    if sku_el:
        sku = sku_el.get_text(strip=True)
        match = re.search(r"\(([^)]+)\)", sku)

        if match:
            product["model_number"] = match.group(1).strip()
        else:
            product["model_number"] = sku

    spans = soup.select(".product-form__selected-value")

    if spans:
        if len(spans) >= 2:
            product["color"] = spans[0].get_text(strip=True)
            product["capacity"] = spans[1].get_text(strip=True)
        elif len(spans) == 1:
            product["capacity"] = spans[0].get_text(strip=True)

    button = soup.select_one(".product-form__payment-container button")

    if button:
        product["available"] = not button.has_attr("disabled")

    return product


def check_stock_status():
    html = fetch_html(PRODUCT_URL)
    soup = parse_html(html)
    return extract_product_data(soup)
