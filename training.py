from chatbot import chatbot

chatbot = Chatbot(sensitivity=.7)
chatbot.train("corpus.json")
