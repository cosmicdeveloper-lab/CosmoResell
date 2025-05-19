from playwright.sync_api import sync_playwright

"""
IMPORTANT:
you need to just run this once to save your facebook profile on playwright
"""


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="fb_state.json")
        page = context.new_page()
        page.goto("https://www.facebook.com/")
        print("⚠️ Please log in manually and close the browser when done.")
        input("Press Enter after logging in and closing any popups...")
        context.storage_state(path="fb_state.json")
        browser.close()


if __name__ == "__main__":
    run()
