from sqlalchemy.dialects.mysql import pymysql

from q_a_system.global_pack import constant
from q_a_system.spacy_play import parts_of_speech
import pymysql

db = pymysql.connect("localhost","Thesis","Thesis123", "QASYSTEM" )
cursor = db.cursor()



def whWord(ques):
    question = constant.nlp(ques)

    questionWord = parts_of_speech.tokenize(question)
    qid=[]
    word=""
    if questionWord[0] in ['How' , 'What','Where', 'When','Which','Who', 'Whom', 'List']:
        word=questionWord[0]

    elif questionWord[0] in ['Show', 'Give']:
        word= "List"
    elif questionWord[0] in ['In','On','To'] and questionWord[1] in ['which','what']:
        word= questionWord[1]
    elif questionWord[0] in ['Do', 'Does', 'Did']:
        word = 'Others'

    cursor.execute("SELECT wid FROM whwords WHERE WHwords =  '" +word +" ' " )
    results = cursor.fetchall()
    for row in results:
        wid = row[0]

    cursor.execute("SELECT qid FROM querieswhwordsrelation WHERE wid =  " + str(wid) )
    results = cursor.fetchall()
    for row in results:
        qid.append(row[0])


    return qid

#print(whWord("Where is the time"))
