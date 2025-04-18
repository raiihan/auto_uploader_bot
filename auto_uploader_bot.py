import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
STORE_CHANNEL_ID = int(os.getenv("STORE_CHANNEL_ID"))
MAIN_BOT_USERNAME = os.getenv("MAIN_BOT_USERNAME")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a file and I’ll create a link to download it!")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.document and not message.video and not message.audio and not message.animation:
        return

    waiting_msg = await message.reply_text("⏳ Uploading to store...")

    sent = await context.bot.copy_message(
        chat_id=STORE_CHANNEL_ID,
        from_chat_id=message.chat_id,
        message_id=message.message_id,
        protect_content=True  # Prevent users from forwarding again
    )

    file_id = sent.message_id
    link = f"https://t.me/{MAIN_BOT_USERNAME}?start={file_id}"

    await waiting_msg.delete()
    await message.reply_text(f"✅ File saved!\n🔗 [Click here to get it]({link})", parse_mode='Markdown')

async def serve_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        try:
            msg_id = int(context.args[0])
            waiting = await update.message.reply_text("⏳ Getting file...")

            file_msg = await context.bot.forward_message(
                chat_id=update.message.chat_id,
                from_chat_id=STORE_CHANNEL_ID,
                message_id=msg_id
            )

            await waiting.delete()

        except Exception as e:
            await update.message.reply_text("❌ File not found or inaccessible.")
    else:
        await update.message.reply_text("❓ Invalid link or file ID.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(
            filters.Document.ALL | filters.Video | filters.Audio | filters.Animation,
            handle_file
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
