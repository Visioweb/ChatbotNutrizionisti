from getpass import getpass
from mysql.connector import connect, Error

def db_connect():
  try:
    connection = connect(
                  host="if7141-001.dbaas.ovh.net",
                  port=35421,
                  user="benessere",
                  password="Callcenter1983",
                  db="benessereevita")
    return connection
  except Error as e:
      print(e)

def notifiche():
  sql = "INSERT INTO notifiche (text, orario) VALUES (%s, %s)"
  val = ("testo", "2021-12-01 15:00:01")
  mycursor.execute(sql, val)

  mydb.commit()
  return True

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


