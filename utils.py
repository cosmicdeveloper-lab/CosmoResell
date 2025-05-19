from statistics import mean
import re
import logging


def filter_cheap_items(items, threshold_ratio):
    """
    :param threshold_ratio:The percentage by which the user wants the item's price to be lower.
    :param items: list of items which facebook or ebay scraper return
    :return: average price and items which are cheaper than the average price
    """

    prices = []
    clean_items = []

    for title, price, link in items:
        try:
            # Remove the currency symbol and any commas/spaces
            price_cleaned = re.sub('[£€$,]', '', price).strip()
            price_float = float(price_cleaned)
            prices.append(price_float)
            clean_items.append((title, price_float, link))
        except ValueError:
            continue  # skip bad price entries

    avg_price = mean(prices) if prices else 0
    cheap_items = [(title, price, link) for title, price, link in clean_items if price < avg_price * threshold_ratio]
    return avg_price, cheap_items


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
