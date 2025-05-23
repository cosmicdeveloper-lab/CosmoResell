<p align="center">
  <img src="https://drive.google.com/uc?id=1at-9o4aDMI5M1CHKJMQvj0-Xsyyk7AN6" alt="CosmoResell Logo" width="200"/>
</p>

<h1 align="center">📦 CosmoResell</h1>

<p align="center">
  A powerful Python-based automation tool for tracking and analyzing item prices on eBay and Facebook Marketplace.
</p>

---

## ✨ Overview

**CosmoResell** helps resellers and enthusiasts automate the process of price tracking for specific items across two major platforms: **eBay** and **Facebook Marketplace**. It scrapes item listings, calculates average prices, and sends customizable alerts via Telegram or a web interface.

---

## 🔧 Features

- 🔍 **Marketplace Scraping**  
  Automatically extract listing data from:
  - eBay
  - Facebook Marketplace (via Playwright)

- 💰 **Price Analysis**  
  Calculates and compares average prices for selected items.

- 📬 **Real-Time Alerts**  
  Sends notifications through:
  - Telegram
  - Web interface (using Quart)

- 🎯 **Custom Threshold Alerts**  
  Define price thresholds and get alerted when deals meet your criteria.

---

## 🧰 Tech Stack

- **Python** 3.9+
- [Playwright](https://playwright.dev/python/)
- [Quart](https://pgjones.gitlab.io/quart/)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

---

## 🚀 Getting Started

### 1. Clone the Repository

 ```bash
git clone https://github.com/cosmicdeveloper-lab/CosmoResell.git
cd cosmoresell
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright

```bash
playwright install
```

### 4. Set Up Environment Variables
  Create a .env file in the root directory with the following:

```bash
TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
```

### 5. Saving Facebook Login Session with Playwright
  Run the script to manually log into Facebook (a browser window will open):

```bash
python save_facebook_profile.py
```
### 6. Run the Script

```bash
python main.py
```

## 📸 Example Signal

Telegram Notification

![CosmoResell Signal Screenshot](https://drive.google.com/uc?id=1OBuLN9P0bnxuF_W9Hop4MOzHbzN9P8hZ)

Web Interface – Search Page

![CosmoResell search page](https://drive.google.com/uc?id=1upmydgaSalTlsAxzppMETrdbLZh4Yd_Y)

Web Interface – Search Results

![CosmoResell search result](https://drive.google.com/uc?id=1jyqcxLX93woLDbfdy1tzQMjrLV2jmwp3)

## 🤝 Contributions

Feel free to fork this repo, open issues, or submit PRs. Any help is appreciated!

## 📄 License

MIT License – see LICENSE file for details.

