from quart import Quart, redirect, render_template, url_for, request
from .forms import MyForm
from core import get_cheap_items
from dotenv import load_dotenv
import os
import logging


logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize the Quart application
app = Quart(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # Required for form CSRF protection


@app.route('/search/', methods=['GET', 'POST'])
async def home():
    """
    Renders and processes the search form.

    On POST: Validates form and redirects to the scrap route with query parameters.
    On GET: Renders the form page.
    """
    form = MyForm(await request.form)

    if await form.validate_on_submit():
        source = form.source.data
        keyword = form.keyword.data
        max_pages = form.max_pages.data
        threshold = form.threshold.data

        # Redirect to the scrap view with all parameters embedded in the URL
        return redirect(url_for('scrap', source=source, keyword=keyword, max_pages=max_pages, threshold=threshold))

    return await render_template('search.html', form=form)


@app.route('/search/<source>/<keyword>/<int:max_pages>/<float:threshold>')
async def scrap(source, keyword, max_pages, threshold):
    """
    Executes the scraping logic and renders the results.

    Parameters passed via URL:
    - source: which scraper to use (e.g. 'ebay', 'facebook')
    - keyword: search query
    - max_pages: how many pages to scrape
    - threshold: price filter

    Returns a rendered HTML list of filtered items.
    """

    logger.info(f"Scraping: source={source}, keyword={keyword}, max_pages={max_pages}, threshold={threshold}")
    items = await get_cheap_items(source, keyword, max_pages, threshold)

    return await render_template('list.html', items=items)


async def start_app():
    """Starts the Quart app on 0.0.0.0:8000 asynchronously."""
    await app.run_task(host="0.0.0.0", port=8000)
