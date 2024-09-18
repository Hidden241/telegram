# bot.py
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import sqlite3
import logging

TOKEN = '7053790577:AAG_NaQSvVP2U2ZKMZh99FyJdgldp-wg4RE'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = user.id
    username = user.username
    first_name = user.first_name

    # Enregistrer l'utilisateur dans la base de données
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name)
        VALUES (?, ?, ?)
    ''', (user_id, username, first_name))
    conn.commit()
    conn.close()

    logger.info("Received /start command from user_id: %s", user_id)
    await update.message.reply_text("Vous avez été enregistré pour le tirage au sort !")
    logger.info("Sent reply to user_id: %s", user_id)

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    logger.info("Starting bot...")
    application.run_polling()
    logger.info("Bot stopped")

if __name__ == "__main__":
    main()
