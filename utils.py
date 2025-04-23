from statistics import mean


def filter_cheap_items(items, threshold_ratio=0.8):
    prices = []
    clean_items = []

    for title, price, link in items:
        try:
            price_float = float(price)
            prices.append(price_float)
            clean_items.append((title, price_float, link))
        except ValueError:
            continue  # skip bad price entries

    avg_price = mean(prices) if prices else 0
    cheap_items = [(title, price, link) for title, price, link in clean_items if price < avg_price * threshold_ratio]
    return avg_price, cheap_items
