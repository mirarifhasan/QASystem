from SPARQLWrapper import SPARQLWrapper, JSON, XML

from q_a_system.api_sevice import mysql_operations
from q_a_system.global_pack import constant


def getQueryResult(propertyList, resourceList, queryIDs):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    answerArray = []

    queries = mysql_operations.getAllSparqlQuery(queryIDs)

    for property in propertyList:
        resource = resourceList[0]
        resource = resource.replace(",", "\,")
        property.property=property.property.replace("/", "\/")
        for query in queries:
            # column traverse for generating Sparql
            sql = ""
            for i in range(3, 12, 1):
                if query[i] == 'res:':
                    sql = sql + " res:" + resource
                elif query[i] == 'dbo/dbp:':
                    sql = sql + " " + property.propertyType + ":" + property.property
                else:
                    sql = sql + " " + query[i]

            print(constant.prefix + sql)
            sparql.setQuery(constant.prefix + sql)
            try:
                if queries in (20,21):
                    sparql.setReturnFormat(XML)
                    results = sparql.query().convert()
                    answerArray.append(results.toxml())
                else:
                    sparql.setReturnFormat(JSON)
                    results = sparql.query().convert()

                    tempResultArray = []
                    for result in results["results"]["bindings"]:
                        tempResultArray.append(result["label"]["value"])
                    answerArray.append(tempResultArray)
            except:
                pass

    return answerArray


