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

TOKEN = os.environ["BOT_TOKEN"]
OWNER_ID = 7411502905

FILTER_FILE = "filters.json"


# =========================
# RENDER WEB SERVER
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
# FILTER STORAGE
# =========================

def load_filters():
    try:
        with open(FILTER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_filters(data):
    with open(FILTER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# =========================
# CHECK OWNER
# =========================

def is_owner(update):
    return (
        update.effective_user
        and update.effective_user.id == OWNER_ID
    )


# =========================
# CHECK MY ID
# =========================

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    await update.message.reply_text(
        f"Your Telegram ID is:\n{user_id}"
    )


# =========================
# ADD FILTER
# =========================

async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):
        await update.message.reply_text(
            "❌ আপনি এই command ব্যবহার করার অনুমতি রাখেন না।"
        )
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ সঠিক নিয়ম:\n\n"
            "/filter keyword reply\n\n"
            "উদাহরণ:\n"
            "/filter hi হাই, কেমন আছেন? 😊"
        )
        return

    keyword = context.args[0].strip().lower()
    reply = " ".join(context.args[1:]).strip()

    data = load_filters()

    data[keyword] = reply

    save_filters(data)

    await update.message.reply_text(
        f"✅ Filter added successfully!\n\n"
        f"Keyword: {keyword}\n"
        f"Reply: {reply}"
    )


# =========================
# DELETE FILTER
# =========================

async def delete_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "ব্যবহার:\n/stop keyword"
        )
        return

    keyword = context.args[0].strip().lower()

    data = load_filters()

    if keyword not in data:
        await update.message.reply_text(
            f"❌ {keyword} নামে কোনো filter পাওয়া যায়নি।"
        )
        return

    del data[keyword]

    save_filters(data)

    await update.message.reply_text(
        f"✅ Filter deleted: {keyword}"
    )


# =========================
# LIST FILTERS
# =========================

async def list_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_owner(update):
        return

    data = load_filters()

    if not data:
        await update.message.reply_text(
            "📋 কোনো filter সেট করা নেই।"
        )
        return

    text = "📋 আপনার Filters:\n\n"

    for keyword, reply in data.items():
        text += f"• {keyword} → {reply}\n"

    await update.message.reply_text(text)


# =========================
# NORMAL MESSAGE REPLY
# =========================

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    if not update.message.text:
        return

    text = update.message.text.strip().lower()

    # FILTER REPLY
    data = load_filters()

    if text in data:
        await update.message.reply_text(data[text])
        return

    # DEFAULT REPLIES
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

app.add_handler(CommandHandler("myid", my_id))
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
