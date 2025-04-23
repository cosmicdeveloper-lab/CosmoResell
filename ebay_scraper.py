import requests
from bs4 import BeautifulSoup
import re


def ebay_scraper(keyword, max_pages=5):
    headers = {"User-Agent": "Mozilla/5.0"}
    items = []

    for page in range(1, max_pages + 1):
        url = f"https://www.ebay.co.uk/sch/i.html?_nkw={keyword}&_pgn={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.select('.s-item')

        for item in listings:
            title_elem = item.select_one('.s-item__title')
            price_elem = item.select_one('.s-item__price')
            link_elem = item.select_one('.s-item__link')

            if not title_elem or not price_elem or not link_elem:
                continue

            title = title_elem.text.strip()
            price_text = price_elem.text.strip()
            link = link_elem.get("href")

            price_match = re.search(r'£([\d,.]+)', price_text)
            if price_match and link:
                try:
                    price = float(price_match.group(1).replace(',', ''))
                    items.append((title, price, link))
                except ValueError:
                    continue

    return items
