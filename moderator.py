## SCRIPT PARA GESTIONAR UN BOT PARA MODERAR UN GRUPO

from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, CommandHandler
import Token
from datetime import datetime
import logging

token = Token.token
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
    )
logger = logging.getLogger()

print('Token:', token)
print('Bot iniciado...')

def start(update: Update, context: CallbackContext) -> None:    # devuelve None

    """ Método para contestar cuando el usuario escriba el comando /start """

    # info del usuario y del chat
    user_id = update.message.from_user.id
    print('user ID:', user_id)
    user_name = update.message.from_user.username
    print('user name:', user_name)
    first_name = update.message.from_user.first_name
    print('first_name:', first_name)
    chat_id = update.message.chat_id
    print('chat ID:', chat_id)

    update.message.reply_text(
        text=f'¡Hola, <b>{user_name}!</b>\n\n'
             f'Puedes escribir los siguientes comandos:\n\n'
             f'<i>/comando1</i> para acción 1\n'
             f'<i>/comando2</i> para acción 2\n'
             f'<i>/comando3</i> para acción 3\n\n'
             f'¡Un saludo!',
        parse_mode='HTML'
    )

def new_member(update: Update, context: CallbackContext) -> None:

    print(update.message.new_chat_members)
    new_member_ID = update.message.new_chat_members[0].id
    new_member_username = update.message.new_chat_members[0].username
    new_member_name = update.message.new_chat_members[0].first_name
    print('ID nuevo miembro:', new_member_ID)
    print('username nuevo miembro:', new_member_username)
    print('name nuevo miembro:', new_member_name)

    update.message.reply_text(f'¡Bienvenido/a al grupo, {new_member_name}!')

def text_response(update: Update, context: CallbackContext) -> None:

    print(type(update.message.text))            # tipo str
    user_text = update.message.text.lower()

    greetings = ['hola', 'hello', 'hi']
    datatimes = ['fecha', 'datetime', 'time', 'hora']

    for word in greetings:
        if word in user_text:
            update.message.reply_text('¡Hola!')

    for word in datatimes:
        if word in user_text:
            now = datetime.now()
            date_time = now.strftime('%d/%m/%y -- %H:%M:%S')

            update.message.reply_text(f'Fecha y hora actuales:  {date_time}')

def ban_words(update: Update, context: CallbackContext) -> None:

    # info del usuario y del chat
    user_id = update.message.from_user.id
    print('user ID:', user_id)
    user_name = update.message.from_user.username
    print('user name:', user_name)
    first_name = update.message.from_user.first_name
    print('first_name:', first_name)
    chat_id = update.message.chat_id
    print('chat ID:', chat_id)
    message_id = update.message.message_id
    user_text = update.message.text
    user_text=user_text.lower()

    banned_words = []

    for word in banned_words:
        if word in user_text:
            try:
                context.bot.delete_message(
                    chat_id=chat_id,
                    message_id=message_id
                )
                context.bot.send_message(
                    chat_id=chat_id,
                    text=f'El usuario {user_name} ha enviado un mensaje que contiene la palabra {word}, que ha sido eliminada.'
                )
                logger.info(f'El usuario {user_name} ha enviado un mensaje que contiene la palabra {word}, que ha sido eliminada.')

            except Exception as error:
                print(error)

def main():

    updater = Updater(token)
    print('updater creado')
    dp = updater.dispatcher
    print('Dispatcher creado')

    dp.add_handler(CommandHandler(
        command='start',
        callback=start
    ))

    dp.add_handler(MessageHandler(
        filters=Filters.status_update.new_chat_members,
        callback=new_member
    ))

    dp.add_handler(MessageHandler(
        filters=Filters.text,
        callback=text_response
    ))

    # palabras prohibidas
    dp.add_handler(MessageHandler(
        filters=Filters.text,
        callback=ban_words
    ))

    updater.start_polling(2)    # listo para escuchar cada 2 segundos
    updater.idle()              # el bot se queda escuchando

main()
