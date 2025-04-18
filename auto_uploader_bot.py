import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram.ext import ContextTypes

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
STORE_CHANNEL_ID = "-1002676143465"  # Your private store channel ID

# Setup logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Auto Upload Bot!")

# File handler
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.video or update.message.audio
    if file:
        file_id = file.file_id
        # You can save or process the file here as per your need
        await update.message.reply_text(f"Received file: {file.file_name}")
        # Send the file back to users on request, or generate deep link if needed
    else:
        await update.message.reply_text("Sorry, I could not process that.")

# Main function to set up the bot
async def main():
    # Create application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handler
    app.add_handler(CommandHandler("start", start))

    # Add file handler for different file types (documents, videos, etc.)
  application.add_handler(MessageHandler(filters.ATTACHMENT, handle_file))


    # Start the bot
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
