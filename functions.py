from mysql.connector import connect, Error   #serve per la function db_connect()
import json #serve per la function creaCorpusDaDatabase
import boto3 #serve per la function estraiTestoImg
import csv #serve per la function insertConversation
from datetime import datetime #serve per la function insertConversation


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





# questa addestra
def creaCorpusDaDatabase():
    class create_dict(dict):

      # __init__ function
      def __init__(self):
        self = dict()

        # Function to add key:value

      def add(self, key, value):
        self[key] = value

    intents = []
    mydict = create_dict()

    rows = []
    samples = []
    responses = []

    select_employee = """
      SELECT
          nome,
          domanda,
          risposta
      FROM
          intent AS inte
      JOIN domanda AS dom
      ON
          inte.id = dom.idIntent
      JOIN risposta AS ris
      ON
          inte.id = ris.idIntent
    """

    db = db_connect()
    cursor = db.cursor()
    cursor.execute(select_employee)
    result = cursor.fetchall()

    temp_row = result[0][0]


    def add_last_intent():
      intents.append({
        "name": temp_row,
        "samples": samples,
        "responses": responses
      })
      mydict.add("intents", intents)


    for row in result:

      if temp_row != row[0]:
        add_last_intent()
        temp_row = row[0]
        samples = []
        responses = []

      if row[0] not in rows:
        rows.append(row[0])

      if row[1] not in samples:
        samples.append(row[1])

      if row[2] not in responses:
        responses.append(row[2])

    mydict['samples'] = ', '.join(mydict['samples'])
    mydict['responses'] = ', '.join(mydict['responses'])
    add_last_intent()
    stud_json = json.dumps(mydict, indent=4, sort_keys=True)
    f = open("corpus.json", "w")
    f.write(stud_json)
    f.close()
    return "Abbiamo addestrato il modello"


#estrai testo con textract da jpg
def estraiTestoImg(doc):
    aws_access_key_id = 'AKIAZDURW7H4GNXDFXPO'
    aws_secret_access_key = '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'
    region_name = 'us-west-1'
    bucket_name = 'textract-console-eu-west-1-fab80e66-32fe-4513-b191-85ededfde858'
    # url esempi: https://github.com/aws-samples/amazon-textract-code-samples
    '''
    Mostrare tutti gli oggetti/files nel bucket 

    s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
    my_bucket = s3.Bucket(bucket_name)

    for file in my_bucket.objects.all():
        print(file.key)
    '''
    documentName = doc
    # Read document content
    with open(documentName, 'rb') as document:
        imageBytes = bytearray(document.read())
    # Amazon Textract client
    textract = boto3.client('textract', aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key, region_name=region_name)
    # Call Amazon Textract
    response = textract.detect_document_text(Document={'Bytes': imageBytes})
    '''
    # Print detected text
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print('\033[94m' + item["Text"] + '\033[0m')
    '''
    return response


def addestraCorpus(corpus_name, sensitivity):
    chatbot = Chatbot(sensitivity=sensitivity)
    chatbot.train(corpus_name)
    return true;



if __name__ == '__main__':
  # Per testare
  vars = creaCorpusDaDatabase()
  print(vars)