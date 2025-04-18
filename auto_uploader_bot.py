import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

# Load environment variables from .env
load_dotenv()

# Get sensitive values from the environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
STORE_CHANNEL_ID = os.getenv("STORE_CHANNEL_ID")
MAIN_BOT_USERNAME = os.getenv("MAIN_BOT_USERNAME")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message.document and not message.video:
        await message.reply_text("Please send or forward a document or video.")
        return

    # Forward to store room
    sent_msg = await context.bot.copy_message(
        chat_id=STORE_CHANNEL_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )

    msg_id = sent_msg.message_id
    deep_link = f"https://t.me/{MAIN_BOT_USERNAME}?start={msg_id}"

    await message.reply_text(f"✅ File saved in Store Room!\n\nHere’s your deep link:\n{deep_link}")

# Define main application
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.Document.ALL | filters.Type.VIDEO | filters.Type.AUDIO | filters.Type.ANIMATION,
        handle_file
    ))

    print("Uploader bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
