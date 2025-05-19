from playwright.async_api import async_playwright


async def ebay_scraper(keyword, max_pages):
    """
    Scrapes Ebay Marketplace for items matching a given keyword.

    Parameters:
    ----------
    keyword : str
        The search keyword to use on Ebay Marketplace.
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
    items = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Set False to see the browser
        context = await browser.new_context()
        page = await context.new_page()

        for page_num in range(1, max_pages + 1):
            search_url = f"https://www.ebay.co.uk/sch/i.html?_nkw={keyword}&_pgn={page_num}"
            print(f"[INFO] Navigating to: {search_url}")
            await page.goto(search_url, timeout=60000)

            # Wait for results to load
            await page.wait_for_selector(".s-item")

            # Extract data from the page
            listings = await page.query_selector_all(".s-item")

            for item in listings:
                title_el = await item.query_selector(".s-item__title")
                price_el = await item.query_selector(".s-item__price")
                link_el = await item.query_selector(".s-item__link")

                if title_el and price_el and link_el:
                    title = await title_el.inner_text()
                    price = await price_el.inner_text()
                    link = await link_el.get_attribute("href")

                    # Skip promotional or non-product items
                    if "Shop on eBay" in title or not link:
                        continue

                    # Normalize for keyword check
                    norm_title = title.lower().replace(" ", "")
                    norm_keyword = keyword.lower().replace(" ", "")

                    if norm_keyword not in norm_title:
                        continue

                    # Clean price (e.g., remove £ and commas)
                    import re
                    match = re.search(r"[£€$]([\d,.]+)", price)
                    if match:
                        clean_price = match.group(1).replace(",", "")
                        items.append((title.strip(), clean_price, link.strip()))

        await browser.close()
    return items
