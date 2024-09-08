import asyncio
import logging
import os

from telegram import Update
from telegram.ext import (
    filters,
    ApplicationBuilder,
    ContextTypes, 
    CommandHandler,
    MessageHandler
)

from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TELEGRAM_API_TOKEN')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.args)
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

if __name__ == '__main__':
    if token:
        application = ApplicationBuilder().token(token).build()
        
        start_handler = CommandHandler('start', start)
        caps_handler = CommandHandler('caps', caps)
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
        
        application.add_handler(start_handler)
        application.add_handler(caps_handler)
        application.add_handler(echo_handler)
        
        application.run_polling()