from ebay_scraper import ebay_scraper
from fb_scraper import scrape_facebook_marketplace_items
from utils import filter_cheap_items
from notifier import send_email_alert, send_sms_alert
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    keyword = "iphone 14"
    all_items = []

    # --- eBay ---
    items = ebay_scraper(keyword)
    all_items.extend(items)

    # --- Facebook Marketplace ---
    fb_items = scrape_facebook_marketplace_items(keyword)
    all_items.extend(fb_items)

    # --- Process and Filter ---
    avg_price, cheap_items = filter_cheap_items(all_items)

    if not cheap_items:
        print("No cheap items found today.")

    body_lines = [f"Average Market Price: £{avg_price:.2f}", "Deals found:"]
    for title, price, link in cheap_items:
        body_lines.append(f" - {title} => £{price:.2f} => {link}")
    alert_message = "\n".join(body_lines)

    # --- Send Alerts ---
    while True:
        ans = input("Do you want to receive alerts trough email or sms? 1/2 ")

        if ans == 1:
            send_sms_alert(os.getenv("TO_PHONE"), alert_message, os.getenv("TWILIO_SID"),
                           os.getenv("TWILIO_TOKEN"), os.getenv("FROM_PHONE"))
            break

        elif ans == 2:
            send_email_alert(os.getenv("TO_EMAIL"), "Cheap Devices Alert!", alert_message, os.getenv("FROM_EMAIL"),
                             os.getenv("EMAIL_PASS"), os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT"))
            break

        else:
            print("Please enter 1 or 2.")
