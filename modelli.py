from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from modelli import *
from datetime import datetime


app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://benessere:Callcenter1983@if7141-001.dbaas.ovh.net:35421/benessereevita'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Creating model table for our CRUD database
class clienti(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    '''idStanza = db.Column(db.Integer, db.ForeignKey('stanze.id'),
        nullable=False)
    stanze = db.relationship('stanze', backref=db.backref('clienti', lazy=True))'''
    codCliente = db.Column(db.String(25))
    nome = db.Column(db.String(255))
    cognome = db.Column(db.String(255))
    dataCheckIn = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dataCheckOut = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    note = db.Column(db.Text, nullable=True)

    def __init__(self, codCliente, nome, cognome, dataCheckIn, dataCheckOut, note):

        self.codCliente = codCliente
        self.nome = nome
        self.cognome = cognome
        self.dataCheckIn = dataCheckIn
        self.dataCheckOut = dataCheckOut
        self.note = note





#Creating model table for our CRUD database
class stanze(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pin = db.Column(db.String(20))
    numero = db.Column(db.Integer)
    nome = db.Column(db.String(255), nullable=True)
    prezzo = db.Column(db.Float, nullable=True)
    descrizione = db.Column(db.Text, nullable=True)
    capacitaMax = db.Column(db.Integer, nullable=True)
    posCamera = db.Column(db.Text, nullable=True)
    quadratura = db.Column(db.Float, nullable=True)
    numVani = db.Column(db.Integer, nullable=True)
    numAccessori = db.Column(db.Integer, nullable=True)
    numLettiMatrimoniale = db.Column(db.Integer, nullable=True)
    numLettiSingolo = db.Column(db.Integer, nullable=True)
    numLettiCastello = db.Column(db.Integer, nullable=True)
    note = db.Column(db.Text, nullable=True)



    def __init__(self, pin, numero, nome, prezzo, descrizione, capacitaMax, posCamera, quadratura, numVani, numAccessori, numLettiMatrimoniale, numLettiSingolo, numLettiCastello, note):

        self.pin = pin
        self.numero = numero
        self.nome = nome
        self.prezzo = prezzo
        self.descrizione = descrizione
        self.capacitaMax = capacitaMax
        self.posCamera = posCamera
        self.quadratura = quadratura
        self.numVani = numVani
        self.numAccessori = numAccessori
        self.numLettiMatrimoniale = numLettiMatrimoniale
        self.numLettiSingolo = numLettiSingolo
        self.numLettiCastello = numLettiCastello
        self.note = note





#Creating model table for our CRUD database
class servizi(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tipologia = db.Column(db.String(255))
    nome = db.Column(db.String(255), nullable=True)
    descrizione = db.Column(db.Text, nullable=True)
    funzionamento = db.Column(db.Text, nullable=True)
    prezzo = db.Column(db.Float, nullable=True)
    note = db.Column(db.Text, nullable=True)



    def __init__(self, tipologia, nome, descrizione, funzionamento, prezzo, note):

        self.tipologia = tipologia
        self.nome = nome
        self.descrizione = descrizione
        self.funzionamento = funzionamento
        self.prezzo = prezzo
        self.note = note





#Creating model table for our CRUD database
class prenotazioni(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(255), nullable=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    durata = db.Column(db.String(255), nullable=True)
    turnazione = db.Column(db.String(255), nullable=True)
    note = db.Column(db.Text, nullable=True)



    def __init__(self, nome, data, durata, turnazione, note):
        self.nome = nome
        self.data = data
        self.durata = durata
        self.turnazione = turnazione
        self.note = note