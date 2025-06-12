from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ChatAction
import os
from telegram.ext import MessageHandler, filters
import httpx
from io import BytesIO


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello from your photo frame bot!")


async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    filename = None
    mime_type = None

    await context.bot.forward_message(
        chat_id=int(os.getenv("TELEGRAM_FORWARD_TO_ID")),
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )


    if update.message.photo:
        # Get the best quality photo
        media = update.message.photo[-1]
        filename = "photo.jpg"
        mime_type = "image/jpeg"
    elif update.message.video:
        media = update.message.video
        filename = "video.mp4"
        mime_type = "video/mp4"
    else:
        return await update.message.reply_text("⚠️ Please send a photo or video.")

    # Notify user bot is working
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_DOCUMENT)

    file = await media.get_file()
    file_bytes = BytesIO()
    await file.download_to_memory(out=file_bytes)
    file_bytes.seek(0)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/upload",
                files={"file": (filename, file_bytes, mime_type)}
            )
        if response.status_code == 200:
            await update.message.reply_text("✅ Media uploaded to your frame!")
        else:
            await update.message.reply_text(f"❌ Upload failed: {response.text}")
    except Exception as e:
        await update.message.reply_text(f"💥 Error: {str(e)}")


async def run_telegram_bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_media))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

