# Openbox Restock Alert

A Python script that sends alerts to one or more email addresses when a tracked [openbox.ca](https://openbox.ca) product comes back in stock.

### How it works:
1. **Scrapes product data:** Requests the product URL, extracts the product data from the page and returns it as a product dictionary
2. **Checks Availability:** Evaluates whether the "Add to cart" button is active and the product is available.
3. **State Management (No Spam):** Uses [Upstash Redis](https://upstash.com) to log whether an alert has already been sent. If an alert went out during a previous run and the product is still available, it skips sending another one.
4. **Email Notification:** If the product transitions from "Out of Stock" to "Available", an email alert is sent out to your recipient list via SMTP.

### Dependencies
-   `python-dotenv` – For loading environment variables.

-   `curl_cffi` – For handling HTTP requests to bypass basic anti-bot scraping blocks.
  
-   `beautifulsoup4` – For parsing the HTML product pages.
  
-   `upstash_redis` – For serverless HTTP-based Redis state management for alerts.

### Configuration

1. **Target Product**
   -   `PRODUCT_URL`: The full URL of the [openbox.ca](https://openbox.ca) product you want to track.
   
       ```env
       PRODUCT_URL="https://openbox.ca/products/apple-iphone-17-unlocked-new-90-day-warranty"
       ```

2. **Email Notification Settings (SMTP)**
   
    Configure your outgoing mail server details:

   -   `SMTP_HOST`: Your SMTP server address (e.g., `smtp.example.com`).
    
   -   `SMTP_PORT`: The port used by your SMTP provider.
    
   -   `SMTP_USER`: The email address sending the alerts.
    
   -   `SMTP_PASSWORD`: The password for the sender email.
    
   -   `RESTOCK_EMAIL_LIST`: A comma-separated list of recipient email addresses.

       ```env
       RESTOCK_EMAIL_LIST="user1@example.com,user2@example.com"
       ```

3. **Upstash Redis State Settings**

    Get these credentials from your [Upstash Console](https://console.upstash.com/):

   -   `UPSTASH_REDIS_REST_URL`: Your database REST URL endpoint.
        
   -   `UPSTASH_REDIS_REST_TOKEN`: Your database REST authentication token.


### Quick Start

1. Clone the repository and navigate into it:

    ```bash
    git clone https://github.com/matthew-sherman/openbox-restock-alert.git
    cd openbox-restock-alert
    ```

2. Install the dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment:

    Create a `.env` file based on the [Configuration](#configuration) section above.

4. Run the script:

    ```bash
    python main.py
    ```

### Automation (GitHub Actions)

Run this script automatically on a schedule using GitHub Actions.

1. **Add Repository Secrets:** Go to your repository **Settings > Secrets and variables > Actions** and add all the variables from the [Configuration](#configuration) section as repository secrets.
2. **Enable the Workflow:** The repository includes a `.github/workflows/restock-monitor.yml` file that runs the script automatically every 30 minutes