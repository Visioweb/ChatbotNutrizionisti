from telegram.ext import Updater,CallbackContext,Filters,Dispatcher,MessageHandler
from telegram import Update

from chatbot import Chatbot


def bot_ask(update:Update,context:CallbackContext):
    print('Messaggio ricevuto:',update.effective_message.text)
    print('Context attuale:',context.chat_data.get('context'))
    chatbot = Chatbot(sensitivity=0.4)
    chatbot.load()
    response,new_context,_ = chatbot.ask(update.effective_message.text, current_context=context.chat_data.get('context'), return_proba=True)
    context.chat_data['context']=new_context
    update.effective_message.reply_text(response)

updater = Updater('1740966801:AAG1LokqUbSVAi0cKzIRvPFUY1kAVFaAYd8')
dispatcher:Dispatcher=updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.text&Filters.chat_type.private, bot_ask))

updater.start_polling()
updater.idle()