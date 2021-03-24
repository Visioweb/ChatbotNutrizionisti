from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from chatbot import Chatbot
from flask_cors import CORS
from actions import *




#app.debug = True
app = Flask(__name__)
CORS(app)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    return render_template('index.html', msg='')






@app.route('/ask', methods=["GET", "POST"])
def ask():

    data = request.get_json()

    if not data or "message" not in data:
       return jsonify({"message":"please specify a message"}), 400

    chatbot = Chatbot(sensitivity=0.7)
    chatbot.load()
    chatbot.add_action("SearchNutritionists", search_nutritionists)
    answer = chatbot.ask(data["message"], return_proba=True)

    return jsonify({"answer": str(answer[0]),
                    "probability": str(answer[1])}), 200
