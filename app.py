from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from chatbot import Chatbot
from flask_cors import CORS
from actions import *
import json


app = Flask(__name__)
CORS(app)

# token per pushare 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

@app.route('/ask', methods=["GET", "POST"])
def ask():

    data = request.get_json()

    if not data:
        return jsonify({"message":"No payload received"}), 400
    if("message" not in data):
       return jsonify({"message":"please specify a message"}), 400

    if("current_context" not in data):
        current_context = None
    else:
        current_context = data["current_context"]

    chatbot = Chatbot(sensitivity=0.4)
    chatbot.load()
    '''
    chatbot.add_action("NutrizionistaCittaIntent", search_nutritionists)
    chatbot.add_action("DietistaCittaIntent", search_dietisti)
    chatbot.add_action("DietologoCittaIntent", search_dietologi)
    '''
    answer = chatbot.ask(data["message"], current_context=current_context, return_proba=True)

    return jsonify({"answer": str(answer[0]),
                    "new_context": str(answer[1]),
                    "probability": str(answer[2])}), 200