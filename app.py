from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from chatbot import Chatbot
from actions import *
import json
from flask_sqlalchemy import SQLAlchemy
from modelli import *


app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://benessere:Callcenter1983@if7141-001.dbaas.ovh.net:35421/benessereevita'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


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
    chatbot.add_action("DietistaCittaIntent", search_dietisti)
    chatbot.add_action("DietologoCittaIntent", search_dietologi)
    answer = chatbot.ask(data["message"], current_context=current_context, return_proba=True)

    return jsonify({"answer": str(answer[0]),
                    "new_context": str(answer[1]),
                    "probability": str(answer[2])}), 200





@app.route('/')
def Index():

    return render_template("index.html")


@app.route('/flow')
def Flow():

    return render_template("flow.html")

@app.route('/clienti')
def Clienti():
    all_clienti = clienti.query.all()

    return render_template("clienti.html", employees = all_clienti)


#this route is for inserting data to mysql database via html forms
@app.route('/clienti/insert', methods = ['GET', 'POST'])
def insertClienti():

    if request.method == 'POST':

        codCliente = request.form['codCliente']
        nome = request.form['nome']
        cognome = request.form['cognome']
        dataCheckIn = request.form['dataCheckIn']
        dataCheckOut = request.form['dataCheckOut']
        note = request.form['note']

        my_data = clienti(codCliente, nome, cognome, dataCheckIn, dataCheckOut, note)
        db.session.add(my_data)
        db.session.commit()

        flash("Clienti Inseriti correttamente")

        return redirect(url_for('Clienti'))


#this is our update route where we are going to update our employee
@app.route('/clienti/update', methods = ['GET', 'POST'])
def updateClienti():

    if request.method == 'POST':
        my_data = clienti.query.get(request.form.get('id'))

        my_data.codCliente = request.form['codCliente']
        my_data.nome = request.form['nome']
        my_data.cognome = request.form['cognome']
        my_data.dataCheckIn = request.form['dataCheckIn']
        my_data.dataCheckOut = request.form['dataCheckOut']
        my_data.note = request.form['note']

        db.session.commit()
        flash("Clienti aggiornati correttamente")

        return redirect(url_for('Clienti'))




#This route is for deleting our employee
@app.route('/clienti/delete/<id>/', methods = ['GET', 'POST'])
def deleteClienti(id):
    my_data = clienti.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Cliente cancellato correttamente")

    return redirect(url_for('Clienti'))








@app.route('/stanze')
def Stanze():
    all_stanze = stanze.query.all()

    return render_template("stanze.html", rooms = all_stanze)



#this route is for inserting data to mysql database via html forms
@app.route('/stanze/insert', methods = ['GET', 'POST'])
def insertStanze():

    if request.method == 'POST':

        pin = request.form['pin']
        numero = request.form['numero']
        nome = request.form['nome']
        prezzo = request.form['prezzo']
        descrizione = request.form['descrizione']
        capacitaMax = request.form['capacitaMax']
        posCamera = request.form['posCamera']
        quadratura = request.form['quadratura']
        numVani = request.form['numVani']
        numAccessori = request.form['numAccessori']
        numLettiMatrimoniale = request.form['numLettiMatrimoniale']
        numLettiSingolo = request.form['numLettiSingolo']
        numLettiCastello = request.form['numLettiCastello']

        note = request.form['note']

        my_data = stanze(pin, numero, nome, prezzo, descrizione, capacitaMax, posCamera, quadratura, numVani, numAccessori, numLettiMatrimoniale, numLettiSingolo, numLettiCastello, note)
        db.session.add(my_data)
        db.session.commit()

        flash("Stanza Inserita correttamente")

        return redirect(url_for('Stanze'))


#this is our update route where we are going to update our employee
@app.route('/stanze/update', methods = ['GET', 'POST'])
def updateStanze():

    if request.method == 'POST':
        my_data = stanze.query.get(request.form.get('id'))

        my_data.pin = request.form['pin']
        my_data.numero = request.form['numero']
        my_data.nome = request.form['nome']
        my_data.prezzo = request.form['prezzo']
        my_data.descrizione = request.form['descrizione']
        my_data.capacitaMax = request.form['capacitaMax']
        my_data.posCamera = request.form['posCamera']
        my_data.quadratura = request.form['quadratura']
        my_data.numVani = request.form['numVani']
        my_data.numAccessori = request.form['numAccessori']
        my_data.numLettiMatrimoniale = request.form['numLettiMatrimoniale']
        my_data.numLettiSingolo = request.form['numLettiSingolo']
        my_data.numLettiCastello = request.form['numLettiCastello']
        my_data.note = request.form['note']

        db.session.commit()
        flash("Stanza aggiornata correttamente")

        return redirect(url_for('Stanze'))




#This route is for deleting our employee
@app.route('/stanze/delete/<id>/', methods = ['GET', 'POST'])
def deleteStanze(id):
    my_data = stanze.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Stanza cancellata correttamente")

    return redirect(url_for('Stanze'))







@app.route('/servizi')
def Servizi():
    all_servizi = servizi.query.all()

    return render_template("servizi.html", services = all_servizi)


#this route is for inserting data to mysql database via html forms
@app.route('/servizi/insert', methods = ['GET', 'POST'])
def insertServizi():

    if request.method == 'POST':
        tipologia = request.form['tipologia']
        nome = request.form['nome']
        descrizione = request.form['descrizione']
        funzionamento = request.form['funzionamento']
        prezzo = request.form['prezzo']
        note = request.form['note']
        my_data = servizi(tipologia, nome, descrizione, funzionamento, prezzo, note)
        db.session.add(my_data)
        db.session.commit()

        flash("Servizi Inseriti correttamente")

        return redirect(url_for('Servizi'))


#this is our update route where we are going to update our employee
@app.route('/servizi/update', methods = ['GET', 'POST'])
def updateServizi():

    if request.method == 'POST':
        my_data = servizi.query.get(request.form.get('id'))
        my_data.tipologia = request.form['tipologia']
        my_data.nome = request.form['nome']
        my_data.descrizione = request.form['descrizione']
        my_data.funzionamento = request.form['funzionamento']
        my_data.prezzo = request.form['prezzo']
        my_data.note = request.form['note']

        db.session.commit()
        flash("Servizi aggiornati correttamente")

        return redirect(url_for('Servizi'))




#This route is for deleting our employee
@app.route('/servizi/delete/<id>/', methods = ['GET', 'POST'])
def deleteServizi(id):
    my_data = servizi.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Servizio cancellato correttamente")

    return redirect(url_for('Servizi'))





@app.route('/prenotazioni')
def Prenotazioni():
    all_prenotazioni = prenotazioni.query.all()

    return render_template("prenotazioni.html", prenotations = all_prenotazioni)


#this route is for inserting data to mysql database via html forms
@app.route('/prenotazioni/insert', methods = ['GET', 'POST'])
def insertPrenotazioni():

    if request.method == 'POST':
        nome = request.form['nome']
        data = request.form['data']
        durata = request.form['durata']
        turnazione = request.form['turnazione']
        note = request.form['note']
        my_data = prenotazioni(nome, data, durata, turnazione, note)
        db.session.add(my_data)
        db.session.commit()

        flash("Prenotazioni Inserite correttamente")

        return redirect(url_for('Prenotazioni'))


#this is our update route where we are going to update our employee
@app.route('/prenotazioni/update', methods = ['GET', 'POST'])
def updatPrenotazioni():

    if request.method == 'POST':
        my_data = prenotazioni.query.get(request.form.get('id'))
        my_data.nome = request.form['nome']
        my_data.data = request.form['data']
        my_data.durata = request.form['durata']
        my_data.turnazione = request.form['turnazione']
        my_data.note = request.form['note']

        db.session.commit()
        flash("Prenotazioni aggiornati correttamente")

        return redirect(url_for('Prenotazioni'))




#This route is for deleting our employee
@app.route('/prenotazioni/delete/<id>/', methods = ['GET', 'POST'])
def deletePrenotazioni(id):
    my_data = prenotazioni.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Prenotazione cancellata correttamente")

    return redirect(url_for('Prenotazioni'))
