from getpass import getpass
from mysql.connector import connect, Error

def db_connect():

  # questa funzione ci permette
  # di collegarci al db mysql

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

def search_nutritionists(vars):

  db = db_connect()
  cursor = db.cursor()

  cursor.execute("SELECT * FROM utente WHERE provincia = '%s' ORDER BY id DESC LIMIT 1" % vars["LOC"])

  result = cursor.fetchall()

  for nutritionist in result:
    # in questo caso prendiamo solo il primo nutrizionista
    # non ho capito nel tuo db qual è il campo relativo al nome
    vars["NUTR"] = nutritionist[12]

  return vars

# Per testare
if _name_ == "__main:__":
  vars = search_nutritionists({"LOC":"Roma"})
  print(vars)
