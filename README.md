# CosmoResell

## CosmoResell is a Python-based automation tool that helps you track the prices of specific items on eBay and Facebook Marketplace. It scrapes listings using Selenium (for eBay) and Playwright (for Facebook Marketplace), calculates the average price, and sends an SMS or email notification with relevant item links.
🔧 Features

## 🔍 Scrape item listings from:

# eBay (using Selenium)
# Facebook Marketplace (using Playwright)
# 💰 Calculate the average price of a specific item
# 📬 Notify you via:
# SMS (via Twilio or similar service)
# Email (SMTP supported)
# ⚙️ Configurable search queries

## 🧰 Tech Stack

# Python 3.9+
# Selenium for eBay scraping
# Playwright for Facebook Marketplace scraping
# Twilio for SMS notifications (optional)
# SMTP for email notifications

## 🚀 Getting Started

# 1. Clone the Repository

 ```bash
git clone https://github.com/yourusername/item-price-notifier.git
cd item-price-notifier
```
# 2. Install Dependencies

```bash
pip install -r requirements.txt
playwright install
```

# 3. Set Up Environment Variables

```bash
ITEM_NAME=your_item_name
EMAIL_SENDER=your@email.com
EMAIL_RECEIVER=receiver@email.com
EMAIL_PASSWORD=yourpassword
USE_SMS=true
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE=your_twilio_phone_number
USER_PHONE=recipient_phone_number
```
# 4. Saving Facebook Login Session with Playwright, This will launch a browser window. Log into your Facebook account manually.

```bash
python save_facebook_profile.py
```
# 5. Run the Script

```bash
python main.py
```
## 📤 Notification Output

# After processing, the script will:
  Print average price in the console
    Send an SMS or email with:
        Links to relevant listings
        The calculated average price

## 📌 TODOs

# Add support for more marketplaces
# Store previous prices for trend analysis
# Add CLI options for search term and notification type

## 🤝 Contributions

# Feel free to fork this repo, open issues, or submit PRs. Any help is appreciated!

## 📄 License

# MIT License – see LICENSE file for details.

