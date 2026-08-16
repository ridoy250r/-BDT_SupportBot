from openai import OpenAI
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"তুমি একটি বাংলা Telegram AI Bot"},
            {"role":"user","content":text}
        ]
    )

    await update.message.reply_text(
        response.choices[0].message.content
    )

app = Application.builder().token(
    os.getenv("BOT_TOKEN")
).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle)
)

app.run_polling()
