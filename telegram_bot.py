from apt.auth import update
from telegram.ext import Updater, CallbackContext, Filters, Dispatcher, MessageHandler, CommandHandler
from telegram import Update, ChatAction, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
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
    #print('Messaggio ricevuto:', update.effective_message.text)
    #print('Context attuale:', context.chat_data.get('context'))

    chatbot = Chatbot(sensitivity=0.4)
    chatbot.load()
    #
    response, new_context, _, intent = chatbot.ask(update.effective_message.text,
                                           current_context=context.chat_data.get('context'),
                                           return_proba=True)

    query_db(update.effective_user.id, intent, update.effective_message.text)

    if intent=='Sconosciuto':
        if context.chat_data.get('intent_sconosciuto', 0)==1:
            update.effective_message.reply_text('Ti passo un operatore')
            context.bot.send_message(
                1002946854,
                f'L\'utente {update.effective_user.mention_html()} ha bisogno di aiuto:\n\nQuesta è la sua conv: \n\n'
                f'{ultimeConvUtente(update.effective_user.id)}',
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Aiuta l\'utente', url=f'tg://user?id={update.effective_user.id}')]])
            )
        else:
            context.chat_data['intent_sconosciuto'] = context.chat_data.get('intent_sconosciuto', 0)+1
            context.chat_data['context'] = new_context
            update.effective_message.reply_text(response)
    else:
        context.chat_data['context'] = new_context
        update.effective_message.reply_text(response)
        context.chat_data['intent_sconosciuto'] = 0

def query_db(userid, intent, text):
    print(userid, intent, text) #qui inserire o selezionare i vari intent


def ultimeConvUtente(userid):
    print(userid)
    #query ultimi 5 records dell utente userid mi deve restituire una stringa non un'array dove c'è la conversazione


@typing()
def start(update: Update, context: CallbackContext):
    msgs = [
        'Salve, sono Andrea, il concierge virtuale di Baia Marticana. Le do il benvenuto! Per accedere al servizio e continuare a chattare, ho bisogno del codice di prenotazione. E’ un numero di 6 cifre, che dovrebbe aver ricevuto via email. Per favore, lo scriva a continuazione.\n'
        'Hello, I\'m Andrea, the virtual concierge of Baia Marticana. Welcome! To access the service and continue chatting, I need your booking code. It\'s a 6-digit number, which you should have received by email. Please write it down as you go along. '
    ]
    update.effective_message.reply_text(
        choice(msgs)
    )

'''
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
'''

@typing()
def salutigenerici(update: Update, context: CallbackContext):
    messgs = [
        'Salve, come posso esserle utile?'
    ]
    update.effective_message.reply_text(
        choice(messgs)
    )


@typing()
def salutigiorno(update: Update, context: CallbackContext):
    messgs = [
        'Buongiorno, come posso aiutarla?'
    ]
    update.effective_message.reply_text(
        choice(messgs)
    )


@typing()
def salutinotte(update: Update, context: CallbackContext):
    messgs = [
        'Buonasera, come posso aiutarla?'
    ]
    update.effective_message.reply_text(
        choice(messgs)
    )

updater = Updater('1740966801:AAEdTnF2FQETbN8SO8i1Y67kO0QgYXPwc5k')
dispatcher: Dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start, Filters.chat_type.private))

'''
dispatcher.add_handler(MessageHandler(Filters.chat_type.private & Filters.text(["no", "No", "no grazie", "No Grazie",
                                                                                "No grazie", "non mi serve altro",
                                                                                "Niente", "niente", "nient'altro", "Non voglio fare niente",
                                                                                "Non ho bisogno di nulla", "Non mi serve nient'altro",
                                                                                "non ho bisogno di nulla", "non ho bisogno di null'altro",
                                                                                "Nient'altro grazie", "nient'altro grazie"]),
                                      nointent))
'''

dispatcher.add_handler(MessageHandler(Filters.text & Filters.chat_type.private, bot_ask))

updater.start_polling()
updater.idle()