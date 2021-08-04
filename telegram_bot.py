from telegram.ext import Updater, CallbackContext, Filters, Dispatcher, MessageHandler, CommandHandler
from telegram import Update
from random import choice

from chatbot import Chatbot


def bot_ask(update: Update, context: CallbackContext):
    print('Messaggio ricevuto:', update.effective_message.text)
    print('Context attuale:', context.chat_data.get('context'))
    chatbot = Chatbot(sensitivity = 0.4)
    chatbot.load()
    response, new_context, _ = chatbot.ask(update.effective_message.text,
                                           current_context = context.chat_data.get('context'),
                                           return_proba = True)
    context.chat_data['context'] = new_context
    update.effective_message.reply_text(response)


def start(update: Update, context: CallbackContext):
    msgs = [
        'Salve sono Andrea, il virtual Concierge di Baia Marticana.\n Posso darle informazioni sulla struttura o turistiche o prendere segnalazioni relative alla camera. Come posso aiutarla?',
        'Salve sono Andrea, il virtual Concierge, le do il benvenuto in Baia Marticana.\n Può chiedermi informazioni turistiche o sulla struttura e fare segnalazioni relative alla camera. Come posso essere utile?'
    ]
    update.effective_message.reply_text(
        choice(msgs)
    )


updater = Updater('1740966801:AAG1LokqUbSVAi0cKzIRvPFUY1kAVFaAYd8')
dispatcher: Dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.text & Filters.chat_type.private, bot_ask))

dispatcher.add_handler(CommandHandler('start', start, Filters.chat_type.private))

updater.start_polling()
updater.idle()