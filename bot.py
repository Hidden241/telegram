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
    
    # Créer la table si elle n'existe pas déjà
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            username TEXT,
            first_name TEXT
        )
    ''')
    
    # Vérifier si l'utilisateur est déjà inscrit
    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0] + 1  # La position actuelle de l'utilisateur
    
    c.execute('''
        INSERT INTO users (user_id, username, first_name)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO NOTHING
    ''', (user_id, username, first_name))
    
    if c.rowcount == 0:
        message = f"You are already registered. There are currently {total_users - 1} participants. Please be patient."
    else:
        message = f"Welcome to 𝐆𝐔𝐌𝐈 and the 𝐅𝐫𝐨𝐤𝐮𝐳𝐚, a legend in the making! You are the {total_users}th participant."
    
    conn.commit()
    conn.close()

    logger.info("Received /start command from user_id: %s", user_id)
    await update.message.reply_text(message)
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
