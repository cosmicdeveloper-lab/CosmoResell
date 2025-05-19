from ebay_scraper import ebay_scraper
from fb_scraper import scrape_facebook_marketplace_items
from utils import filter_cheap_items


async def get_cheap_items(source, keyword, max_pages, threshold_ratio):
    """
    :param source: marketplace
    :param keyword: item
    :param max_pages: how many pages to scrape
    :param threshold_ratio: The percentage by which the user wants the item's price to be lower.
    :return: average price of a specified items and the items which are cheaper than the
    ratio that user defined
    """

    if source == 'facebook':
        fb_items = await scrape_facebook_marketplace_items(keyword, max_pages)
        avg_price, cheap_items = filter_cheap_items(fb_items, threshold_ratio)
        return avg_price, cheap_items

    elif source == 'ebay':
        ebay_items = await ebay_scraper(keyword, max_pages)
        avg_price, cheap_items = filter_cheap_items(ebay_items, threshold_ratio)
        return avg_price, cheap_items
