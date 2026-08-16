from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = "এখানে_আপনার_BOT_TOKEN"

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "hello" in text:
        await update.message.reply_text("Hello! কেমন আছেন?")
    elif "support" in text:
        await update.message.reply_text("Support এর জন্য অ্যাডমিনের সাথে যোগাযোগ করুন।")
    elif "payment" in text:
        await update.message.reply_text("Payment সংক্রান্ত সমস্যার বিস্তারিত লিখুন।")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

app.run_polling()
