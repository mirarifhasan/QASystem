from SPARQLWrapper import SPARQLWrapper, JSON, XML

from q_a_system.api_sevice import mysql_operations
from q_a_system.global_pack import constant


def getQueryResult(propertyList, resourceList, queryIDs,question):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    answerArray = []

    questionWords = question.split(' ')
    questionWords[-1] = questionWords[-1].replace("?","")
    for word in questionWords:
        if word in ['top', 'maximum']:
            queryIDs = [22]
        elif word in ['total']:
            queryIDs = [23]
        elif word in ['average']:
            queryIDs = [24]

    queries = mysql_operations.getAllSparqlQuery(queryIDs)

    for property in propertyList:
        resource = resourceList[0]
        resource = resource.replace(",", "\,")
        resource = resource.replace(".", "\.")
        resource = resource.replace("+", "\+")
        resource = resource.replace("(", "\(")
        resource = resource.replace(")", "\)")
        property.property=property.property.replace("/", "\/")
        for query in queries:
            # column traverse for generating Sparql
            sql = ""
            for i in range(3, 20, 1):
                if query[i] == 'res:':
                    sql = sql + " res:" + resource
                elif query[i] == 'dbo/dbp:':
                    sql = sql + " " + property.propertyType + ":" + property.property
                else:
                    sql = sql + " " + query[i]

            print(constant.prefix + sql)
            sparql.setQuery(constant.prefix + sql)
            try:
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                if query[0] in (20,21):
                    answerArray.append(results['boolean'])
                else:
                    tempResultArray = []
                    for result in results["results"]["bindings"]:
                        tempResultArray.append(result["label"]["value"])
                    answerArray.append(tempResultArray)
            except:
                pass

    return answerArray


