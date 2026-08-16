import os

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ["BOT_TOKEN"]

REPLIES = {
    "hello": "Welcome to our group",
    "bonus": "আজকের বোনাস ৫০ টাকা",
    "support": "সাপোর্টের জন্য অ্যাডমিনকে মেসেজ করুন",
    "payment": "পেমেন্ট সমস্যার বিস্তারিত লিখুন",
}

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text.lower()

        if text in REPLIES:
            await update.message.reply_text(REPLIES[text])


app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply)
)

app.run_polling()
