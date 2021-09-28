from getpass import getpass
from mysql.connector import connect, Error
from datetime import datetime as dt
import re


def db_connect():
  try:
    connection = connect(
                  host="if7141-001.dbaas.ovh.net",
                  port=35421,
                  user="benessere",
                  password="Callcenter1983",
                  db="Hotel")
    return connection
  except Error as e:
      print(e)

def notifiche():
  sql = "INSERT INTO notifiche (text, orario) VALUES (%s, %s)"
  val = ("testo", "2021-12-01 15:00:01")
  mycursor.execute(sql, val)

  mydb.commit()
  return True


def siCodice(text, userid):
    def si_codice(vars):
        db = db_connect()
        cursor = db.cursor()
        formatted_date = dt.now().strftime("%Y/%m/%d %H:%M:%S")

        codCliente = ''.join([str(temp) for temp in text if temp.isdigit()])
        print(codCliente)

        cursor.execute(
            "SELECT nome, cognome FROM clienti WHERE codCliente = '%s'" % codCliente)
        result = cursor.fetchall()

        if (cursor.rowcount == 0):
            vars['NominativoCliente'] = None
        else:
            vars['NominativoCliente'] = ' '.join([riga[0] + ' ' + riga[1] for riga in result])
            print(vars['NominativoCliente'])
            sqlco = "INSERT INTO conversazioni (telegram_id, codCliente, dataora) VALUES (%s, %s, %s)"
            valco = (userid, codCliente, formatted_date)
            cursor.execute(sqlco, valco)
            db.commit()
            idconve = cursor.lastrowid
            print(idconve)

        return vars
    return si_codice

def noCodEscalation(text, userid):
    def nocodEsc(vars):
        db = db_connect()
        cursor = db.cursor()
        match = re.search(r'[\w\.-]+@[\w\.-]+', text)
        email_address = match.group(0)
        print(email_address)
        #fare query select per prelevare codCliente
        cursor.execute(
            "SELECT codCliente FROM clienti WHERE email = '%s'" % email_address)
        result = cursor.fetchall()
        print(result)

        if (cursor.rowcount == 0):
            vars['codCliente'] = None
        else:
            vars['codCliente'] = ''.join([riga[0] for riga in result])
            print(vars['codCliente'])

            sqlco = "INSERT INTO conversazioni (telegram_id, codCliente, dataora) VALUES (%s, %s, %s)"
            valco = (userid, vars['codCliente'], formatted_date)
            cursor.execute(sqlco, valco)
            db.commit()
            idconve = cursor.lastrowid
            print(idconve)

        return vars
    return nocodEsc

'''
def search_nutritionists(vars):
  db = db_connect()
  cursor = db.cursor()

  cursor.execute("SELECT * FROM utente WHERE roles LIKE '%%ROLE_NUTRIZIONISTA%%' and provincia = '%s' ORDER BY id DESC LIMIT 1" % vars["LOC"])
  result = cursor.fetchall()

  if(cursor.rowcount==0):
    vars["NUTR"] = "nessuno"
  else:
    for nutritionist in result:
      print(nutritionist[12])
      # in questo caso prendiamo solo il primo nutrizionista
      # non ho capito nel tuo db qual è il campo relativo al nome
      vars["NUTR"] = nutritionist[12]

  return vars


def search_dietisti(vars):
  db = db_connect()
  cursor = db.cursor()

  cursor.execute("SELECT * FROM utente WHERE roles LIKE '%%ROLE_DIETISTA%%' and provincia = '%s' ORDER BY id DESC LIMIT 1" % vars["LOC"])
  result = cursor.fetchall()

  if(cursor.rowcount==0):
    vars["DIET"] = "nessuno"
  else:
    for dietist in result:
      print(dietist[12])
      # in questo caso prendiamo solo il primo nutrizionista
      # non ho capito nel tuo db qual è il campo relativo al nome
      vars["DIET"] = dietist[12]

  return vars


def search_dietologi(vars):
  db = db_connect()
  cursor = db.cursor()

  cursor.execute("SELECT * FROM utente WHERE roles LIKE '%%ROLE_DIETOLOGO%%' and provincia = '%s' ORDER BY id DESC LIMIT 1" % vars["LOC"])
  result = cursor.fetchall()

  if(cursor.rowcount==0):
    vars["DIGO"] = "nessuno"
  else:
    for dietol in result:
      print(dietol[12])
      # in questo caso prendiamo solo il primo nutrizionista
      # non ho capito nel tuo db qual è il campo relativo al nome
      vars["DIGO"] = dietol[12]

  return vars
'''


