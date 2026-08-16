import os
import json

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ["BOT_TOKEN"]
OWNER_ID = 7411502905

FILTER_FILE = "filters.json"


def load_filters():
    try:
        with open(FILTER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_filters(data):
    with open(FILTER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "ব্যবহার করুন:\n/filter keyword reply"
        )
        return

    keyword = context.args[0].lower()
    reply = " ".join(context.args[1:])

    data = load_filters()
    data[keyword] = reply
    save_filters(data)

    await update.message.reply_text(
        f"✅ Filter added!\n\n"
        f"Keyword: {keyword}\n"
        f"Reply: {reply}"
    )


async def delete_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "ব্যবহার করুন:\n/stop keyword"
        )
        return

    keyword = context.args[0].lower()

    data = load_filters()

    if keyword not in data:
        await update.message.reply_text(
            f"❌ `{keyword}` নামে কোনো filter নেই।",
            parse_mode="Markdown"
        )
        return

    del data[keyword]
    save_filters(data)

    await update.message.reply_text(
        f"✅ `{keyword}` filter deleted.",
        parse_mode="Markdown"
    )


async def list_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    data = load_filters()

    if not data:
        await update.message.reply_text("এখনো কোনো filter সেট করা হয়নি।")
        return

    text = "📋 আপনার Filters:\n\n"

    for keyword, reply in data.items():
        text += f"• {keyword} → {reply}\n"

    await update.message.reply_text(text)


async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower().strip()

    data = load_filters()

    if text in data:
        await update.message.reply_text(data[text])


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("filter", add_filter))
app.add_handler(CommandHandler("stop", delete_filter))
app.add_handler(CommandHandler("filters", list_filters))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        auto_reply
    )
)

app.run_polling()
