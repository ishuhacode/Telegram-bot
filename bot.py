from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

TOKEN = "8632557200:AAHFhTSDYi6GaAoh3rH99qdkfprd1xqUHiE"
ADMIN_ID = 8220335817  # apna Telegram user ID daal

GROUP_LINK = "https://t.me/+qmzZEvH3vGowNThl"


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Proof text
    await update.message.reply_text("Proof 👇")

    # Proof image
    await update.message.reply_photo(photo=open("proof.jpg", "rb"))

    # Proof video
    await update.message.reply_video(video=open("proof.mp4", "rb"))

    # Message
    message_text = """✅ I earned 2500💲 in 22 day's
No course no time waste 😎

Only 88rs
Lifetime access 
Weakly updated content

😄 Directly send you my trick just copy paste my methods and Start earning by yourself.💰💚

Do smart work:- 🔥
• 5 PDFs. 
• Fully step by step.  
• one time setup.
• earn while you are sleeping.
• Genuine way to earn.

Join my team now 🤟🏻

Send screenshot of the payment I'll add you."""

    # Buttons
    keyboard = [
        [InlineKeyboardButton("Want to Buy ✅", callback_data="buy")],
        [InlineKeyboardButton("No ❌", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(message_text, reply_markup=reply_markup)


# BUTTON HANDLER
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        await query.message.reply_text("UPI QR se payment kare 👇")
        await query.message.reply_photo(photo=open("qr.png", "rb"))
        await query.message.reply_text("Screenshot bhejo, mai verify karke access dunga")

    elif query.data == "no":
        await query.message.reply_text("Theek hai 👍")

    elif "approve" in query.data:
        user_id = int(query.data.split("_")[1])

        await context.bot.send_message(
            chat_id=user_id,
            text=f"Thank you ✅\nYeh raha private group link:\n{GROUP_LINK}"
        )

        await query.edit_message_text("Approved ✅")

    elif "reject" in query.data:
        user_id = int(query.data.split("_")[1])

        await context.bot.send_message(
            chat_id=user_id,
            text="Payment verify nahi hua ❌"
        )

        await query.edit_message_text("Rejected ❌")


# SCREENSHOT HANDLE
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    keyboard = [
        [InlineKeyboardButton("Approve ✅", callback_data=f"approve_{user.id}")],
        [InlineKeyboardButton("Reject ❌", callback_data=f"reject_{user.id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Screenshot admin ko forward
    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"User ID: {user.id}\nPayment screenshot aaya hai",
        reply_markup=reply_markup
    )

    await update.message.reply_text("Screenshot receive ho gaya, verify ho raha hai...")


# MAIN APP
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("Bot running...")
app.run_polling()