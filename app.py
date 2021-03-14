from flask import Flask, request, jsonify
from chatbot import Chatbot
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/ask', METHOD=['POST'])
def ask():

    data = request.get_json()

    if("message" not in data):
        return jsonify({"message":"please specify a message"}), 400

    chatbot = Chatbot()
    chatbot.load()
    answer = chatbot.ask(data["message"], return_proba=True)

    return jsonify({"answer": str(answer[0]),
                    "probability": str(answer[1])}), 200
