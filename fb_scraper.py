from playwright.async_api import async_playwright
import urllib.parse


async def scrape_facebook_marketplace_items(keyword, max_items):
    """
    Scrapes Facebook Marketplace for items matching a given keyword.

    Parameters:
    ----------
    keyword : str
        The search keyword to use on Facebook Marketplace.
    max_items : int
        The maximum number of items to return.

    Returns:
    -------
    List[Tuple[str, str, str]]
        A list of tuples where each tuple contains:
            - title (str): The item's title
            - price (str): The item's price
            - url (str): Direct link to the listing
    """
    user_data_dir = "playwright_profile"
    search_url = f"https://www.facebook.com/marketplace/search/?query={urllib.parse.quote(keyword)}"
    items = []

    async with async_playwright() as p:
        # Use a persistent context to avoid login issues
        browser = await p.firefox.launch_persistent_context(user_data_dir, headless=True)
        page = await browser.new_page()
        await page.goto(search_url)
        await page.wait_for_timeout(5000)  # Wait for dynamic content to load

        # Scroll the page to load more items
        for _ in range(3):
            await page.mouse.wheel(0, 2000)
            await page.wait_for_timeout(1500)

        # Select all listing cards
        cards = await page.query_selector_all('a[href^="/marketplace/item/"]')
        seen_urls = set()

        for card in cards:
            href = await card.get_attribute("href")
            if not href:
                continue

            full_url = urllib.parse.urljoin("https://www.facebook.com", href)
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            try:
                text_block = await card.inner_text()
                text_parts = text_block.strip().split('\n')

                price = text_parts[0].strip() if len(text_parts) > 0 else "N/A"
                title = text_parts[1].strip() if len(text_parts) > 1 else "N/A"
            except Exception as e:
                print(f"Error parsing card: {e}")
                continue

            items.append((title, price, full_url))
            if len(items) >= max_items:
                break

        await browser.close()

    return items
