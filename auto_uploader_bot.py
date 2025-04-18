import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Auto Upload Bot!")

# File handler
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.video or update.message.audio or update.message.animation
    if file:
        await update.message.reply_text(f"Received file: {file.file_name}")
    else:
        await update.message.reply_text("Sorry, I could not process that.")

# Main bot runner
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.document | filters.video | filters.audio | filters.animation,
        handle_file
    ))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

