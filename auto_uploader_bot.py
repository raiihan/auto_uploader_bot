import os
from telegram import Update, MessageEntity
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

BOT_TOKEN = "7760025681:AAELVpPgZn9kDbbtiXvgEz11XW_VdVUYC64"  # Bot token
STORE_CHANNEL_ID = -1002676143465  # Store Room 🏬 Channel ID
MAIN_BOT_USERNAME = "NoSourceFileBot"  # Main file delivery bot username

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a file or forward one. I'll store it and give you a deep link!")

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

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
    filters.Document.ALL | filters.Video | filters.Audio | filters.Animation,
    handle_file ))


    print("Uploader bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
