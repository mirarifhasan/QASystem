from SPARQLWrapper import SPARQLWrapper, JSON
from q_a_system.global_pack import constant

import pymysql

db = pymysql.connect("localhost","Thesis","Thesis123", "QASYSTEM" )
cursor = db.cursor()
cursor.execute("SELECT A FROM templates WHERE id = 2 ")
results = cursor.fetchall()
for row in results:
    a =row[0]

#question = input.getUserQuestion()

def getQueryResult(propertyList, resourceList):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    answerArray = []


    for property in propertyList:
        resource = resourceList[0]

        sql = """ 
            """ + a + resource + """ """ + property.propertyType + """:""" + property.property + """ ?uri }"""

        print(constant.prefix + sql)
        sparql.setQuery(constant.prefix + sql)


        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        tempResultArray = []
        for result in results["results"]["bindings"]:
            tempResultArray.append(result["uri"]["value"])

        answerArray.append(tempResultArray)



    return answerArray

db.close()