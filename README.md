# 📦CosmoResell

CosmoResell is a Python-based automation tool that helps you track the prices of specific items on eBay and Facebook Marketplace

## 🔧 Features

- 🔍 Scrape item listings from:
- eBay and Facebook Marketplace (using Playwright)
- 💰 Calculate the average price of a specific item
- 📬 Notify you via:
- Telegram and web
- defining threshold

## 🧰 Tech Stack

- Python 3.9+
- Playwright
- quart
- python-telegram-bot

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

## 🤝 Contributions

Feel free to fork this repo, open issues, or submit PRs. Any help is appreciated!

## 📄 License

MIT License – see LICENSE file for details.

