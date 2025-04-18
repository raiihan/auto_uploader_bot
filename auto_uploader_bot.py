# auto_uploader_bot.py
import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
STORE_CHANNEL_ID = os.getenv("STORE_CHANNEL_ID")

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Auto Upload Bot!")

# File upload handler
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.video or update.message.audio or update.message.animation
    if file:
        file_id = file.file_id
        file_name = file.file_name or "Unnamed file"
        await update.message.reply_text(f"Received file: {file_name}\nFile ID: {file_id}")
        # TODO: forward to STORE_CHANNEL_ID or generate deep link
    else:
        await update.message.reply_text("Unsupported file type or empty message.")

# Main bot setup
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.VIDEO | filters.DOCUMENT | filters.AUDIO | filters.ANIMATION,
        handle_file
    ))

    # Start polling
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
