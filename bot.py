import os
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# SETTINGS
# =========================

TOKEN = os.environ["BOT_TOKEN"]
OWNER_ID = 7411502905

FILTER_FILE = "filters.json"


# =========================
# RENDER PORT SERVER
# =========================

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, format, *args):
        return


def start_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


threading.Thread(
    target=start_web_server,
    daemon=True
).start()


# =========================
# FILTER DATABASE
# =========================

def load_filters():
    try:
        with open(FILTER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_filters(data):
    with open(FILTER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# =========================
# ADD FILTER
# =========================

async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "ব্যবহার:\n/filter keyword reply"
        )
        return

    keyword = context.args[0].lower().strip()
    reply = " ".join(context.args[1:])

    data = load_filters()
    data[keyword] = reply
    save_filters(data)

    await update.message.reply_text(
        f"✅ Filter added!\n\n"
        f"Keyword: {keyword}\n"
        f"Reply: {reply}"
    )


# =========================
# DELETE FILTER
# =========================

async def delete_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "ব্যবহার:\n/stop keyword"
        )
        return

    keyword = context.args[0].lower().strip()

    data = load_filters()

    if keyword not in data:
        await update.message.reply_text(
            f"❌ {keyword} নামে কোনো filter নেই।"
        )
        return

    del data[keyword]
    save_filters(data)

    await update.message.reply_text(
        f"✅ {keyword} filter deleted."
    )


# =========================
# SHOW FILTERS
# =========================

async def list_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != OWNER_ID:
        return

    data = load_filters()

    if not data:
        await update.message.reply_text(
            "এখনো কোনো filter সেট করা হয়নি।"
        )
        return

    text = "📋 Filters:\n\n"

    for keyword, reply in data.items():
        text += f"• {keyword} → {reply}\n"

    await update.message.reply_text(text)


# =========================
# NORMAL AUTO REPLY
# =========================

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    text = update.message.text.lower().strip()

    # Filter replies
    data = load_filters()

    if text in data:
        await update.message.reply_text(data[text])
        return

    # Default replies
    replies = {
        "hello": "Welcome to our group",
        "bonus": "আজকের বোনাস ৫০ টাকা",
        "support": "সাপোর্টের জন্য অ্যাডমিনকে মেসেজ করুন",
        "payment": "পেমেন্ট সমস্যার বিস্তারিত লিখুন",
    }

    if text in replies:
        await update.message.reply_text(replies[text])


# =========================
# BOT
# =========================

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
