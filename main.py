from alerts import trigger_alert
from scraper import check_stock_status


def main():
    product = check_stock_status()

    if not product or not product.get("name"):
        print("Failed to retrieve product data. Skipping execution.")
        return

    if product.get("available"):
        success_count, failure_count = trigger_alert(product)
        print(f"{success_count} alerts sent.")
        print(f"{failure_count} alerts failed to send.")
    else:
        print(f"{product.get('name')} is currently out of stock!")


if __name__ == "__main__":
    main()
