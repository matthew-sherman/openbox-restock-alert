from alerts import trigger_alert
from scraper import check_stock_status
from state import has_alert_been_sent, set_alert_state


def main():
    product = check_stock_status()

    if not product or not product.get("name"):
        print("Failed to retrieve product data. Skipping execution.")
        return

    if product.get("available"):
        alert_sent = has_alert_been_sent()

        if not alert_sent:
            success_count, failure_count = trigger_alert(product)
            print(f"{success_count} alerts sent.")
            print(f"{failure_count} alerts failed to send.")

            if success_count > 0:
                set_alert_state(True)

        else:
            print(
                f"{product.get('name')} is still in stock, but an alert was already sent."
            )
    else:
        if has_alert_been_sent():
            set_alert_state(False)

        print(f"{product.get('name')} is currently out of stock!")


if __name__ == "__main__":
    main()
