import logging
import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace "YOUR_TELEGRAM_BOT_TOKEN" with your actual bot token obtained from BotFather
TOKEN = "6330275785:AAG_qK16WycWEnfBPcM02OLLw2_4rqNNZ0Y"

# Replace "YOUR_DISCORD_WEBHOOK_URL" with your Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1134736042818277508/07EQr2jfDCQll2Vs7jznHbC0lmlSXtX8PCNnUjJ7JIIbVTB6wQItmFZCVIGciJh_niXH"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to send message via Discord webhook
def send_discord_message(message: str) -> None:
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

# Handler function for the /start command (button)
def start(update: Update, context: CallbackContext) -> None:
    user_name = update.effective_user.first_name

    # Create the buttons
    buttons = [
        [KeyboardButton("/help"), KeyboardButton("/contacts")],
        [KeyboardButton("/prices"), KeyboardButton("/portfolio")],
        [KeyboardButton("/language"), KeyboardButton("/address")],
        [KeyboardButton("/buy"), KeyboardButton("/info")],
        [KeyboardButton("/promotions"), KeyboardButton("/feedback")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons)

    # Send the message with buttons
    update.message.reply_text(f"Hello, {user_name}! Welcome to our photo editing and photography studio. How can we assist you today, dear customer?", reply_markup=reply_markup)

# Handler function for the /help command
def help_command(update: Update, _: CallbackContext) -> None:
    help_text = """
    Available commands:
    /start - Starting the bot and greeting people with "Hello dear customer!!!"
    /help - Show available commands and their functionalities
    /website - Get a link to digitalcrafts.co.uk
    /prices - Show all prices for photo shooting and editing services
    /portfolio - Show 3 photos from the same photo studio but in different angles
    /language - Switch the language between English and Romanian
    /contacts - Get a phone number: +48507430155
    /address - Get the country: UK
    /buy - Purchase a service (replace with actual logic)
    /info - Get general information about our photo editing and photography studio
    /promotions - Check out ongoing promotions and discounts
    /feedback - Provide feedback to the studio
    """
    update.message.reply_text(help_text)

# Handler function for the /website command
def website(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Here is the link to digitalcrafts.co.uk: https://digitalcrafts.co.uk')

# Handler function for the /prices command
def prices(update: Update, _: CallbackContext) -> None:
    prices_text = """
    Prices for our photo services:
    - Photo shooting: $50
    - Photo editing: $30
    - Food photos: $40
    - Family photos: $60
    - Business photos: $80
    - Event photos: $70
    - Product photos: $50
    (and more)
    """
    update.message.reply_text(prices_text)

# Handler function for the /portfolio command
def portfolio(update: Update, _: CallbackContext) -> None:
    # Replace these links with the actual URLs to your portfolio photos
    photo_links = [
        "https://example.com/photo1.jpg",
        "https://example.com/photo2.jpg",
        "https://example.com/photo3.jpg"
    ]
    update.message.reply_text("Here are some portfolio photos:")
    for link in photo_links:
        update.message.reply_photo(photo=link)

# Handler function for the /language command
def language(update: Update, _: CallbackContext) -> None:
    # Implement logic to switch between English and Romanian
    # For this example, we'll simply provide a static response
    update.message.reply_text("Language switched successfully!")

# Handler function for the /contacts command
def contacts(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Contact phone number: +48507430155")

# Handler function for the /address command
def address(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Country: UK")

# Handler function for the /buy command (replace with actual logic)
def buy(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("To purchase a service, please contact us at the provided phone number.")

# Handler function for the /info command
def info(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("We are a professional photo editing and photography studio committed to providing high-quality services to our customers.")

# Handler function for the /promotions command
def promotions(update: Update, _: CallbackContext) -> None:
    promotions_text = "Check out our ongoing promotions and discounts:\n\n" \
                     "- 10% off on all photo shooting packages.\n" \
                     "- 20% off on photo editing services for the first 50 customers.\n" \
                     "- Refer a friend and get 15% off on your next photo session.\n" \
                     "(and more)"
    update.message.reply_text(promotions_text)

# Handler function for the /feedback command
def feedback(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Please provide your valuable feedback, and it will be sent to us via Discord webhook.")
    context.user_data["feedback"] = True

# Function to send feedback via Discord webhook
def send_feedback_via_discord(user_id: int, feedback_text: str) -> None:
    feedback_message = f"Feedback from User ID: {user_id}\n\nFeedback: {feedback_text}"
    send_discord_message(feedback_message)

# Handler function to handle feedback submission
def handle_feedback(update: Update, context: CallbackContext) -> None:
    if "feedback" in context.user_data and context.user_data["feedback"]:
        feedback_text = update.message.text
        user_id = update.message.from_user.id
        send_feedback_via_discord(user_id, feedback_text)
        update.message.reply_text("Thank you for your feedback! It has been sent to us via Discord webhook.")
        context.user_data["feedback"] = False

# ... (continue with the rest of the command handlers)

def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register the command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("website", website))
    dp.add_handler(CommandHandler("prices", prices))
    dp.add_handler(CommandHandler("portfolio", portfolio))
    dp.add_handler(CommandHandler("language", language))
    dp.add_handler(CommandHandler("contacts", contacts))
    dp.add_handler(CommandHandler("address", address))
    dp.add_handler(CommandHandler("buy", buy))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("promotions", promotions))
    dp.add_handler(CommandHandler("feedback", feedback))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_feedback))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C
    updater.idle()

if __name__ == "__main__":
    main()
