"""
Telegram bot for fetching and sending cheap item deals from Facebook Marketplace or eBay.

The user is guided through a conversation to input:
- Source market (facebook or ebay)
- Search keyword
- Number of pages to scrape
- Price threshold ratio

Results are fetched, formatted, and sent to a Telegram chat.
"""

import requests
import re
import os
from dotenv import load_dotenv


from telegram_text import Link
from telegram.ext import Application
from telegram import Update
from telegram.ext import (CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler)
from core import get_cheap_items


# Load env
load_dotenv()
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Conversation states
SOURCE, KEY_WORD, MAX_PAGES, THRESHOLD_RATIO = range(4)


def escape_markdown_v2(text):
    # Escapes Telegram Markdown V2 special characters in the given text.
    escape_chars = r'_*\[\]()~`>#+-=|{}.!,%-'
    return re.sub(f'([{re.escape(escape_chars)}])', '', text)


def format_message(avg_price, cheap_items):
    if not cheap_items:
        return 'No cheap items found.'

    lines = [f'*Average Market Price:* £{avg_price:.2f}\n*Deals found:*\n']

    for title, price, link in cheap_items:
        safe_title = escape_markdown_v2(title)
        formatted_link = Link(safe_title, link)
        safe_price = escape_markdown_v2(f'£{price:.0f}')
        lines.append(f'- {formatted_link} - {safe_price}\n')

    return ''.join(lines)


def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    max_len = 4096
    lines = message.splitlines(keepends=True)
    chunks, chunk = [], ""

    for line in lines:
        if len(chunk) + len(line) > max_len:
            chunks.append(chunk)
            chunk = line
        else:
            chunk += line
    if chunk:
        chunks.append(chunk)

    for c in chunks:
        payload = {
            'chat_id': chat_id,
            'text': c,
            'parse_mode': 'Markdown'
        }
        # Send each message chunk to avoid exceeding Telegram's character limit
        response = requests.post(url, data=payload)
        response.raise_for_status()


# Conversation Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Which market are you looking for?\nType: *facebook* or *ebay*',
                                    parse_mode='MarkdownV2')
    return SOURCE


async def handle_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    if text not in ['facebook', 'ebay']:
        await update.message.reply_text('Please type "facebook" or "ebay".')
        return SOURCE

    context.user_data['source'] = text
    await update.message.reply_text('What are you looking for?')
    return KEY_WORD


async def handle_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['keyword'] = update.message.text.strip()
    await update.message.reply_text('How many pages do you want to extract?')
    return MAX_PAGES


async def handle_max_pages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pages = int(update.message.text.strip())
        context.user_data['max_pages'] = pages
    except ValueError:
        await update.message.reply_text('Please enter a valid number.')
        return MAX_PAGES

    await update.message.reply_text('Enter the threshold ratio as a float (e.g., 0.8, 0.65...):')
    return THRESHOLD_RATIO


async def handle_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        ratio = float(update.message.text.strip())
        if 0 < ratio < 1:
            context.user_data['threshold_ratio'] = ratio
        else:
            await update.message.reply_text('Please enter a valid float between 0 and 1.')

    except ValueError:
        await update.message.reply_text('Please enter a valid float (e.g., 0.8).')
        return THRESHOLD_RATIO

    # Gather all inputs
    source = context.user_data['source']
    keyword = context.user_data['keyword']
    max_pages = context.user_data['max_pages']
    threshold_ratio = context.user_data['threshold_ratio']

    # Fetch and send result
    avg_price, cheap_items = await get_cheap_items(source, keyword, max_pages, threshold_ratio)
    message = format_message(avg_price, cheap_items)
    send_telegram_message(TOKEN, CHAT_ID, message)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Canceled.')
    return ConversationHandler.END


async def start_bot():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SOURCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_source)],
            KEY_WORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_keyword)],
            MAX_PAGES: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_max_pages)],
            THRESHOLD_RATIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_threshold)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    app.add_handler(conv)
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
