from telegram.ext import Updater, CallbackContext, Filters, Dispatcher, MessageHandler, CommandHandler
from telegram import Update, ChatAction
from random import choice
from time import sleep
from chatbot import Chatbot


def typing(secs: int = 1):
    def decorator(func):
        def wrapper(update: Update, context: CallbackContext):
            context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
            sleep(secs)
            func(update, context)

        return wrapper

    return decorator


@typing()
def bot_ask(update: Update, context: CallbackContext):
    print('Messaggio ricevuto:', update.effective_message.text)
    print('Context attuale:', context.chat_data.get('context'))

    chatbot = Chatbot(sensitivity=0.4)
    chatbot.load()
    response, new_context, _ = chatbot.ask(update.effective_message.text,
                                           current_context=context.chat_data.get('context'),
                                           return_proba=True)
    context.chat_data['context'] = new_context
    update.effective_message.reply_text(response)


@typing()
def start(update: Update, context: CallbackContext):
    msgs = [
        'Salve sono Andrea, il virtual Concierge di Baia Marticana.\nPosso darle informazioni sulla struttura, info turistiche o prendere segnalazioni relative alla camera. Come posso aiutarla?',
        'Salve sono Andrea, il virtual Concierge, le do il benvenuto in Baia Marticana.\nPuò chiedermi informazioni turistiche, info sulla struttura e fare segnalazioni relative alla camera. Come posso essere utile?'
    ]
    update.effective_message.reply_text(
        choice(msgs)
    )


@typing()
def nointent(update: Update, context: CallbackContext):
    messgs = [
        'ok, qualunque cosa non esiti a contattarmi.',
        'resto comunque a sua disposizione.',
        'va bene se ha bisogno sono sempre qui, arrivederci.'
    ]
    update.effective_message.reply_text(
        choice(messgs)
    )


updater = Updater('1740966801:AAEdTnF2FQETbN8SO8i1Y67kO0QgYXPwc5k')
dispatcher: Dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start, Filters.chat_type.private))

dispatcher.add_handler(MessageHandler(Filters.chat_type.private & Filters.text(["no", "No", "no grazie", "No Grazie",
                                                                                "No grazie", "non mi serve altro",
                                                                                "Niente", "niente", "Non voglio fare niente",
                                                                                "Non ho bisogno di nulla", "Non mi serve nient'altro",
                                                                                "non ho bisogno di nulla", "non ho bisogno di null'altro"]),
                                      nointent))

dispatcher.add_handler(MessageHandler(Filters.text & Filters.chat_type.private, bot_ask))

updater.start_polling()
updater.idle()