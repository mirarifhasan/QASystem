from SPARQLWrapper import SPARQLWrapper, JSON
from q_a_system.global_pack import constant
from q_a_system.api_sevice import db_connect, mysql_operations


def getQueryResult(propertyList, resourceList, queryIDs):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    answerArray = []

    queries = mysql_operations.getAllSparqlQuery(queryIDs);

    for property in propertyList:
        resource = resourceList[0]

        for query in queries:
            # column traverse for generating Sparql
            sql = ""
            for i in range(3, 8, 1):
                if query[i] == 'res:':
                    sql = sql + " res:" + resource
                elif query[i] == 'dbo/dbp:':
                    sql = sql + " " + property.propertyType + ":" + property.property
                else:
                    sql = sql + " " + query[i]

            print(constant.prefix + sql)
            sparql.setQuery(constant.prefix + sql)

            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            tempResultArray = []
            for result in results["results"]["bindings"]:
                tempResultArray.append(result["label"]["value"])

            answerArray.append(tempResultArray)

    return answerArray
