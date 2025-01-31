import json
import spacy
from random import choice
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import shuffle
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import pickle
import os
import re
from datetime import datetime as dt
from actions import *
import numpy as np



class Chatbot:
    MODEL_FOLDER = "model"
    LOGS_FOLDER = "logs"

    SENSITIVITY = None

    _model = None
    _nlp = None
    _dictionary = None
    _bow = None
    _le = None
    _corpus = None

    _actions_map = {}
    _actions_error_map = {}

    def __init__(self, sensitivity=0.8):
        self._nlp = spacy.load("it_core_news_sm")
        self.SENSITIVITY = sensitivity

        if (not os.path.isdir(self.LOGS_FOLDER)):
            os.mkdir(self.LOGS_FOLDER)
            self._create_log("errors.log")
            self._create_log("conversations.log")

    def add_action(self, intent, action):
        self._actions_map[intent] = action

    def add_error_string(self, intent, error):
        self._actions_error_map[intent] = error



    def ask(self, question, current_context=None, return_proba=False):

        tokens = self._nlp(question)
        entities = {}

        for ent in tokens.ents:
            entities[ent.label_] = ent.text        

        doc = ""

        for token in tokens:

            if (not token.is_punct):
                if token.ent_type_ is not "":
                    doc += " " + str(token.ent_type_).lower()
                elif token.is_stop:
                    continue
                elif token.lemma_ is not None:
                    doc += " " + token.lemma_
                else:
                    doc += " " + token
        
        doc = doc.strip()
        print("DOC: "+"'"+str(doc)+"' QUESTION: "+"'"+str(question)+"'")

        x = self._bow.transform([doc])

        y_proba = self._model.predict([x])[0]
        y_sorted = np.argsort(y_proba)[::-1]
        y_sorted = np.argsort(y_proba)[::-1]

        response = None
        new_context = None
        errore = 0

        for i in range(y_sorted.shape[0]):

            y = y_sorted[i]
            y_proba_max = y_proba[y]

            if y_proba_max < self.SENSITIVITY:
                break

            intent = self._le.inverse_transform([y])[0]
            response, new_context = self._get_response(intent, entities=entities, current_context=current_context)
            
            if response:
                break
            
        if not response:
            response = self._get_default()
            intent = "Sconosciuto"
            errore = 1
            self._save_log(question, response, intent, y_proba_max, error=True)
        
        self._save_conv_db(question, response, intent, y_proba_max, errore, new_context)
        self._save_log(question, response, intent, y_proba_max)

        return (response, new_context, y_proba_max, intent) if return_proba else response


    def train(self, corpus_file, epochs=1000, verbose=True):

        with open(corpus_file) as f:
            self._corpus = json.loads(f.read())  # carichiamo il json in un dict

        self.dictionary, docs, intents = self._clean(self._corpus)
        
        X = self._bagofwords(docs)
        y = self._encoding(intents)
        X, y = shuffle(X, y, random_state=0)  # mescoliamo i dati
        self._model = self._build_dnn(X, y, epochs, verbose)
        self._save()
        

    def load(self):

        # verifichiamo che la cartella esista
        if not os.path.isdir(self.MODEL_FOLDER):
            print("No model found !")
            return

        # carichiamo gli oggetti

        with open(self.MODEL_FOLDER + '/corpus.pk', 'rb') as f:
            self._corpus = pickle.load(f)

        with open(self.MODEL_FOLDER + '/dictionary.pk', 'rb') as f:
            self.dictionary = pickle.load(f)

        with open(self.MODEL_FOLDER + '/bow.pk', 'rb') as f:
            self._bow = pickle.load(f)

        with open(self.MODEL_FOLDER + '/encoder.pk', 'rb') as f:
            self._le = pickle.load(f)

        # importiamo il modello

        self._model = load_model(self.MODEL_FOLDER + "/model")

    def _get_response(self, intent_name, entities=None, current_context=None):

        # cerchiamo una risposta
        # per l'intent

        new_context = None

        for intent in self._corpus["intents"]:
            if intent["name"] == intent_name:
                response = choice(intent["responses"])  # selezioniamo una risposta casualmente
                break

        if "context" in intent:
            if(current_context!=intent["context"]["required"]):
                return None, None
            else:
                new_context = intent["context"]["set"]

        vars = entities
        if intent["name"] in self._actions_map:
            # se c'è una action per l'intent
            # allora la eseguiamo e utilizziamo il dizionario ritornato
            # nella risposta
            vars = self._actions_map[intent["name"]](entities)


        for var in vars:
            if vars[var] == None:
                return choice(self._actions_error_map.get(var, ["non ho trovato nulla"])), current_context

            # sostituiamo i placeholders con il dizionario
            response = response.replace("<" + var + ">", vars[var])


        return response, new_context

    def _get_default(self):
        return choice(self._corpus["defaults"])

    def _clean(self, corpus):

        dictionary = set({})
        intents = []

        docs = []

        for intent in corpus["intents"]:

            for sample in intent["samples"]:

                sample = sample.lower()
                #sample = re.sub(r'\<[^()]*\>', '', sample)  # rimuoviamo i placeholders
                sample = sample.replace("<","").replace(">","")
                tokens = self._nlp(sample)
                doc = ""

                for token in tokens:
                    print("LEMMA con stopwords: " + token.lemma_)
                    f = open("stopwordsi.txt", "w+")
                    f.write(token.lemma_ + "\n")
                    f.close()
                    if (not token.is_punct and not token.is_stop):
                        print("LEMMA senza stopwords: "+token.lemma_)
                        f = open("stopwordno.txt", "a+")
                        f.write(token.lemma_ + "\n")
                        f.close()
                        doc += " " + token.lemma_  # otteniamo il lemma
                        dictionary.add(token.lemma_)  # aggiungiamo al dizionario
                if (len(doc) > 0):
                    docs.append(doc.strip())
                    intents.append(intent["name"])
        return dictionary, docs, intents

    def _save(self):

        # salviamo gli oggetti

        if not os.path.isdir(self.MODEL_FOLDER):
            os.mkdir(self.MODEL_FOLDER)

        with open(self.MODEL_FOLDER + '/corpus.pk', 'wb') as f:
            pickle.dump(self._corpus, f)

        with open(self.MODEL_FOLDER + '/dictionary.pk', 'wb') as f:
            pickle.dump(self._dictionary, f)

        with open(self.MODEL_FOLDER + '/bow.pk', 'wb') as f:
            pickle.dump(self._bow, f)

        with open(self.MODEL_FOLDER + '/encoder.pk', 'wb') as f:
            pickle.dump(self._le, f)

        # esportiamo il modello

        self._model.save(self.MODEL_FOLDER + "/model")

    def _bagofwords(self, docs):
        self._bow = CountVectorizer()
        X = self._bow.fit_transform(docs)
        return X

    def _encoding(self, intents):
        # eseguiamo l'encoding degli intents
        self._le = LabelEncoder()
        y = self._le.fit_transform(intents)
        ohe = OneHotEncoder()
        y = ohe.fit_transform(y.reshape(-1, 1))
        return y

    def _build_dnn(self, X, y, epochs, verbose):

        # definiamo l'architettura della rete
        model = Sequential()
        model.add(Dense(12, activation="relu", input_dim=X.shape[1]))
        model.add(Dense(8, activation="relu"))
        model.add(Dense(y.shape[1], activation="softmax"))
        model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])

        # eseguiamo l'addestramento
        model.fit(X.toarray(), y.toarray(), epochs=epochs, verbose=int(verbose))
        return model

    def _create_log(self, filename):
        f = open(self.LOGS_FOLDER + "/" + filename, "w+")
        f.write("DATA E ORA\tDOMANDA\tRISPOSTA\tINTENT\tPROBABILITA'")
        f.close()

    def _save_log(self, question, answer, intent, proba, error=False):
        
        if (error):
            f = open(self.LOGS_FOLDER + "/errors.log", "a+")
        else:
            f = open(self.LOGS_FOLDER + "/conversations.log", "a+")
      
        date_time = dt.now().strftime("%d/%m/%Y %H:%M:%S")

        f.write("\n" +
                date_time + "\t" +
                question + "\t" +
                answer + "\t" +
                intent + "\t" +
                str(proba)
                )

        f.close()
        
    def _save_conv_db(self, question, answer, intent, proba, errore, contesto, error=False):
        db = db_connect()
        cursor = db.cursor()
        formatted_date = dt.now().strftime("%Y/%m/%d %H:%M:%S")  

        sql = "INSERT INTO conversations (domanda, risposta, intent, probabilita, errore, contesto, dataora) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (question, answer, intent, float(proba), errore, contesto, formatted_date)
        cursor.execute(sql, val)

        db.commit()

        

if __name__ == '__main__':
    from actions import *

    chatbot = Chatbot(sensitivity=.4)
    chatbot.train("andrea_corpus.json", verbose=False)
    chatbot.load()
    answer = chatbot.ask("come va?", return_proba=True)
    print(answer)
