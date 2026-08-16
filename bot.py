from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = "8622176657:AAGH9hOdG9c5lwWmqTp4aAZcbwMIeTQcTUc"

REPLIES = {
    "hello": "Welcome to our group",
    "bonus": "আজকের বোনাস ৫০ টাকা",
    "support": "সাপোর্টের জন্য অ্যাডমিনকে মেসেজ করুন",
    "payment": "পেমেন্ট সমস্যার বিস্তারিত লিখুন"
}

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text in REPLIES:
        await update.message.reply_text(REPLIES[text])

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

app.run_polling()
