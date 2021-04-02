from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from chatbot import Chatbot
from flask_cors import CORS
from actions import *

app = Flask(__name__)
CORS(app)


@app.route('/dashboard')
def home():
    # Check if user is loggedin
    '''
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    '''
    return render_template('home.html')

@app.route('/profile')
def profile():
    # Check if user is loggedin
    #if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
    db = db_connect()
    cursor = db.cursor()
    #cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    cursor.execute('SELECT * FROM accounts WHERE id = 1')
    account = cursor.fetchone()
    # Show the profile page with account info
    return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    #return redirect(url_for('login'))

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
            '''
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            #return 'Logged in successfully!'
            '''
            return redirect(url_for('home'))
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



@app.route('/conversazioni')
def conversation():
    # Check if user is loggedin
    #if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
    db = db_connect()
    cursor = db.cursor()
    #cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    cursor.execute('SELECT * FROM conversations')
    conversation = cursor.fetchall()

    return render_template('conversation.html', conversation=conversation)



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
    chatbot.add_action("NutrizionistaCittaIntent", search_nutritionists)
    answer = chatbot.ask(data["message"], current_context=current_context, return_proba=True)

    return jsonify({"answer": str(answer[0]),
                    "new_context": str(answer[1]),
                    "probability": str(answer[2])}), 200
