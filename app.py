from flask import Flask, request, jsonify
from chatbot import Chatbot
from flask_cors import CORS
from actions import *


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/ask": {"origins": "https://visioweb.it"}})

@app.route('/ask', methods=["GET", "POST"])
@cross_origin(origin='https://visioweb.it',headers=['Content- Type','Authorization'])


'''
app = Flask(__name__)
CORS(app)

@app.route('/ask', methods=["GET", "POST"])
'''
def ask():

    data = request.get_json()

    if("message" not in data):
        return jsonify({"message":"please specify a message"}), 400

    chatbot = Chatbot()
    chatbot.load()
    chatbot.add_action("SearchNutrizionists", search_nutrizionists)
    answer = chatbot.ask(data["message"], return_proba=True)

    return jsonify({"answer": str(answer[0]),
                    "probability": str(answer[1])}), 200
