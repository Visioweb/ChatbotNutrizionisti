from apt.auth import update
from telegram.ext import Updater, CallbackContext, Filters, Dispatcher, MessageHandler, CommandHandler
from telegram import Update, ChatAction, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from random import choice
from time import sleep
from chatbot import Chatbot
from actions import db_connect, siCodice, noCodEscalation
from datetime import datetime as dt



def typing(secs: int = 0.5):
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

    chatbot.add_action("SiCodice", siCodice(update.effective_message.text, update.effective_user.id))
    chatbot.add_error_string("NominativoCliente", ["Il codice inserito è errato o non è nel database, ne provi un altro", "Il codice non è registrato, potrebbe essere errato"])

    chatbot.add_action("NoCodEscalation", noCodEscalation(update.effective_message.text, update.effective_user.id))
    chatbot.add_error_string("codCliente", ["La mail inserita è errata o non è nel nostro database, ne provi un'altra", "La mail non è registrata, potrebbe essere errata"])


    response, new_context, _, intent = chatbot.ask(update.effective_message.text,
                                           current_context=context.chat_data.get('context'),
                                           return_proba=True)

    query_db(update.effective_user.id, intent, update.effective_message.text, response)

    if intent=='Sconosciuto':
        if context.chat_data.get('intent_sconosciuto', 0)==1:
            update.effective_message.reply_text('Attenda un secondo le passo l\'operatore...')
            context.bot.send_message(
                1002946854,
                f'L\'utente {update.effective_user.mention_html()} ha bisogno di aiuto:\n\nQuesta è la sua conversazione: \n\n'
                f'{ultimeConvUtente(update.effective_user.id)}',
                parse_mode=ParseMode.HTML
            )
        else:
            context.chat_data['intent_sconosciuto'] = context.chat_data.get('intent_sconosciuto', 0)+1
            context.chat_data['context'] = new_context
            update.effective_message.reply_text(response)
    else:
        context.chat_data['context'] = new_context
        update.effective_message.reply_text(response)
        context.chat_data['intent_sconosciuto'] = 0

def query_db(userid, intent, text, response):
    print(userid, intent, text) #qui inserire o selezionare i vari intent
    db = db_connect()
    cursor = db.cursor()
    formatted_date = dt.now().strftime("%Y/%m/%d %H:%M:%S")
    contesto = None
    risposta = response

    cursor.execute("SELECT id, codCliente FROM conversazioni WHERE telegram_id = '%s' ORDER BY id DESC LIMIT 1" % userid)
    result = cursor.fetchall()


    probabilita = 0
    errore = 0
    for res in result:
        idconve = res[0]
        codCliente = res[1]

    sql = "INSERT INTO conversations (idConversazioni, telegram_id, codCliente, domanda, risposta, intent, probabilita, errore, contesto, dataora) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (idconve, userid, codCliente, text, risposta, intent, probabilita, errore, contesto, formatted_date)
    cursor.execute(sql, val)

    db.commit()


    #INSERT INTO `wallet`(`id`, `idStanza`, `idCliente`, `causale`, `prezzo`, `data`, `note`, `dataInserimento`)
    if intent == 'WalletBarColazione' or intent == 'WalletBarGelato' or intent == 'WalletBarBibite':
        cursor.execute(
            "SELECT id, idStanza FROM clienti WHERE codCliente = '%s' ORDER BY id DESC LIMIT 1" % codCliente)
        resultcl = cursor.fetchall()

        prezzo = 0
        note = ''
        for recl in resultcl:
            idCliente = recl[0]
            idStanza = recl[1]
        sqlw = "INSERT INTO wallet (`idStanza`, `idCliente`, `causale`, `prezzo`, `data`, note) VALUES (%s, %s, %s, %s, %s, %s)"
        valw = (idStanza, idCliente, text, prezzo, formatted_date, note)
        cursor.execute(sqlw, valw)

        db.commit()


def ultimeConvUtente(userid):
    print(userid)
    #query ultimi 5 records dell utente userid mi deve restituire una stringa non un'array dove c'è la conversazione
    db = db_connect()
    cursor = db.cursor()
    cursor.execute("SELECT domanda, risposta FROM conversations WHERE telegram_id = '%s' ORDER BY id DESC LIMIT 5" % userid)
    result = cursor.fetchall()

    if (cursor.rowcount == 0):
        conve = "nessuno"
    else:
        conve = '\n\n'.join([f'L\'utente ha scritto: {riga[0]}\nIl chatbot ha risposto: {riga[1]}' for riga in result])


    return conve



@typing()
def start(update: Update, context: CallbackContext):
    msgs = [
        'Salve, sono Andrea, il concierge virtuale di Baia Marticana. Le do il benvenuto! Per accedere al servizio e continuare a chattare, ho bisogno del codice di prenotazione. E’ un numero di 6 cifre, che dovrebbe aver ricevuto via email. Per favore, lo scriva a continuazione.\n'
        #'Hello, I\'m Andrea, the virtual concierge of Baia Marticana. Welcome! To access the service and continue chatting, I need your booking code. It\'s a 6-digit number, which you should have received by email. Please write it down as you go along. '
    ]
    update.effective_message.reply_text(
        choice(msgs)
    )


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


dispatcher.add_handler(MessageHandler(Filters.text & Filters.chat_type.private, bot_ask))

updater.start_polling()
updater.idle()