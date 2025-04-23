from playwright.sync_api import sync_playwright
import urllib.parse


def scrape_facebook_marketplace_items(keyword: str, max_items: int = 20) -> list:
    user_data_dir = "playwright_profile"
    search_url = f"https://www.facebook.com/marketplace/search/?query={urllib.parse.quote(keyword)}"
    items = []

    with sync_playwright() as p:
        browser = p.firefox.launch_persistent_context(user_data_dir, headless=True)  #Turn False if you want to see the browser
        page = browser.new_page()
        page.goto(search_url)
        page.wait_for_timeout(5000)

        for _ in range(3):
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(1500)

        cards = page.query_selector_all('a[href^="/marketplace/item/"]')

        seen_urls = set()

        for card in cards:
            href = card.get_attribute("href")
            full_url = urllib.parse.urljoin("https://www.facebook.com", href)

            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            try:
                text_block = card.inner_text()
                text_parts = text_block.strip().split('\n')
                price = text_parts[0].strip() if len(text_parts) > 0 else "N/A"
                title = text_parts[1].strip() if len(text_parts) > 1 else "N/A"

                items.append({
                    "title": title,
                    "price": price,
                    "url": full_url
                })

            except Exception as e:
                print(f"Error parsing card: {e}")

            if len(items) >= max_items:
                break

        browser.close()

    return items
