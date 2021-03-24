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
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        
        db = db_connect()
        cursor = db.cursor()

        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))





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
