import os
import psycopg2
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import logging

# Récupération du token depuis les variables d'environnement
TOKEN = '7053790577:AAG_NaQSvVP2U2ZKMZh99FyJdgldp-wg4RE'
DATABASE_URL = os.getenv('DATABASE_URL')

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Retourne une connexion à la base de données PostgreSQL."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

async def start(update: Update, context: CallbackContext):
    """Gestionnaire de la commande /start."""
    user = update.effective_user
    user_id = user.id
    username = user.username
    first_name = user.first_name

    # Enregistrer l'utilisateur dans la base de données
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            username TEXT,
            first_name TEXT
        )
    ''')
    c.execute('''
        INSERT INTO users (user_id, username, first_name)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO NOTHING
    ''', (user_id, username, first_name))
    conn.commit()
    conn.close()

    logger.info("Received /start command from user_id: %s", user_id)
    await update.message.reply_text("test test test !")
    logger.info("Sent reply to user_id: %s", user_id)

def main():
    """Fonction principale pour démarrer le bot."""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    logger.info("Starting bot...")
    application.run_polling()
    logger.info("Bot stopped")

if __name__ == "__main__":
    main() 
