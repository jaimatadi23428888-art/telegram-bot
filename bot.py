import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# आपका बॉट टोकन
TOKEN = "8889793288:AAGbU6Jc_FpFznfl-P122L8nt2jLQxUx6tI"

# आपकी UPI ID और नाम
UPI_ID = "abhishekpandey23422@axl"
NAME = "Saurabh Pandey"

# यहाँ अपने QR Code की इमेज का फाइल नेम या डायरेक्ट लिंक डाल सकते हैं (जैसे 'qr.jpg')
# सुनिश्चित करें कि यह इमेज आपकी स्क्रिप्ट वाले फोल्डर में 'qr.jpg' नाम से सेव हो
QR_IMAGE_PATH = "qr.jpg" 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔑 Purchase Key", callback_data='purchase')],
        [InlineKeyboardButton("🔑 My Keys", callback_data='my_keys')],
        [InlineKeyboardButton("🔄 Reset Key", callback_data='reset_key')],
        [InlineKeyboardButton("📞 Contact Support", callback_data='support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "👋 **Welcome to the Official Key Bot!**\n\n"
        "Use the menu buttons below to purchase a key, "
        "view your active keys, or reset device HWID."
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'purchase':
        # स्क्रीनशॉट के अनुसार सभी रेट्स सेट किए गए हैं
        keyboard = [
            [InlineKeyboardButton("⏱️ 2 Hours — ₹24.00", callback_data='plan_24')],
            [InlineKeyboardButton("⏱️ 5 Hours — ₹49.00", callback_data='plan_49')],
            [InlineKeyboardButton("⏱️ 1 Days — ₹89.00", callback_data='plan_89')],
            [InlineKeyboardButton("⏱️ 3 Days — ₹160.00", callback_data='plan_160')],
            [InlineKeyboardButton("⏱️ 7 Days — ₹299.00", callback_data='plan_299')],
            [InlineKeyboardButton("⏱️ 14 Days — ₹390.00", callback_data='plan_390')],
            [InlineKeyboardButton("⏱️ 30 Days — ₹550.00", callback_data='plan_550')],
            [InlineKeyboardButton("⏱️ 60 Days — ₹749.00", callback_data='plan_749')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("🛒 **Select Key Duration:**", reply_markup=reply_markup, parse_mode='Markdown')

    elif query.data.startswith('plan_'):
        # प्लान के हिसाब से कीमत तय करना
        prices = {
            'plan_24': ("2 Hours", "₹24.00"),
            'plan_49': ("5 Hours", "₹49.00"),
            'plan_89': ("1 Days", "₹89.00"),
            'plan_160': ("3 Days", "₹160.00"),
            'plan_299': ("7 Days", "₹299.00"),
            'plan_390': ("14 Days", "₹390.00"),
            'plan_550': ("30 Days", "₹550.00"),
            'plan_749': ("60 Days", "₹749.00")
        }
        
        duration, amount = prices.get(query.data, ("1 Days", "₹89.00"))

        caption_text = (
            "🗂️ **BILLING SUMMARY**\n\n"
            "🎮 **Application:** PUBG/BGMI Mobile\n"
            f"⏳ **Duration:** {duration}\n"
            f"💳 **Total Payable:** {amount}\n"
            f"🆔 **UPI ID:** {UPI_ID}\n\n"
            "👇 *Scan the QR code above using PhonePe, Paytm, GPay, or any UPI App to pay.*\n\n"
            "⚠️ **Important:** Click '✅ I have paid' below after completing transaction to instantly get your key."
        )
        
        pay_keyboard = [[InlineKeyboardButton("✅ I have paid", callback_data='paid_confirm')]]
        pay_markup = InlineKeyboardMarkup(pay_keyboard)

        # यूजर के पास QR Code की फोटो और साथ में बिलिंग समरी भेजना
        try:
            with open(QR_IMAGE_PATH, 'rb') as photo_file:
                await query.message.reply_photo(
                    photo=photo_file,
                    caption=caption_text,
                    reply_markup=pay_markup,
                    parse_mode='Markdown'
                )
        except Exception:
            # अगर फोटो फाइल फोल्डर में न मिले तो केवल टेक्स्ट समरी भेज देगा
            await query.message.reply_text(
                "⚠️ **QR Code image not found on server!**\n\n" + caption_text,
                reply_markup=pay_markup,
                parse_mode='Markdown'
            )

    elif query.data == 'paid_confirm':
        await query.message.reply_text("✅ Payment verification under process. Your key will be delivered shortly: `MOD-KEY-SAMPLE`", parse_mode='Markdown')

    elif query.data == 'my_keys':
        await query.message.reply_text("🔑 You have no active keys right now.", parse_mode='Markdown')

    elif query.data == 'reset_key':
        await query.message.reply_text("🔄 Send your key to reset its HWID/Device.", parse_mode='Markdown')

    elif query.data == 'support':
        await query.message.reply_text("📞 Contact Owner for support.", parse_mode='Markdown')

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is running successfully...")
    app.run_polling()

if __name__ == '__main__':
    main()