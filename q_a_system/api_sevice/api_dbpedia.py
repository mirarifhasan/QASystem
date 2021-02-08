from SPARQLWrapper import SPARQLWrapper, JSON, XML
import numpy as np
from q_a_system.api_sevice import mysql_operations
from q_a_system.global_pack import constant
from q_a_system.spacy_play import property_selection


def makeZeroResSql(propertyList, query):
    sqls = []

    if query[2] == 2:
        ind = len(propertyList) - 1
        for prop1 in propertyList[ind]:
            for prop2 in propertyList[ind]:
                sql = ''
                dboDbpCount = 0
                for i in range(3, 20, 1):
                    if query[i] == 'dbo/dbp:':
                        if dboDbpCount == 0:
                            sql = sql + " " + prop1.propertyType + ":" + prop1.property
                            dboDbpCount = dboDbpCount + 1
                        elif dboDbpCount == 1:
                            sql = sql + " " + prop2.propertyType + ":" + prop2.property
                    else:
                        sql = sql + " " + query[i]
                sqls.append(sql)

    if query[2] == 3:
        ind = len(propertyList) - 1
        for prop1 in propertyList[ind]:
            for prop2 in propertyList[ind]:
                for prop3 in propertyList[ind]:
                    sql = ''
                    dboDbpCount = 0
                    for i in range(3, 20, 1):
                        if query[i] == 'dbo/dbp:':
                            if dboDbpCount == 0:
                                sql = sql + " " + prop1.propertyType + ":" + prop1.property
                                dboDbpCount = dboDbpCount + 1
                            elif dboDbpCount == 1:
                                sql = sql + " " + prop2.propertyType + ":" + prop2.property
                                dboDbpCount = dboDbpCount + 1
                            elif dboDbpCount == 2:
                                sql = sql + " " + prop3.propertyType + ":" + prop3.property
                        else:
                            sql = sql + " " + query[i]
                    sqls.append(sql)

    return list(property_selection.removeDuplicates(sqls))


def makeOneResSql(propertyList, resourceList, query):
    sqls = []

    if query[2] == 1:
        for i, resource in enumerate(resourceList):
            for prop1 in propertyList[i]:
                sql = ''
                for i in range(3, 20, 1):
                    if query[i] == 'res:':
                        sql = sql + " res:" + resource
                    elif query[i] == 'dbo/dbp:':
                        sql = sql + " " + prop1.propertyType + ":" + prop1.property
                    else:
                        sql = sql + " " + query[i]
                sqls.append(sql)

    if query[2] == 2:
        for i, resource in enumerate(resourceList):
            for prop1 in propertyList[i]:
                for propLast in propertyList[len(resourceList)]:
                    sql = ''
                    for i in range(3, 20, 1):
                        if query[i] == 'res:':
                            sql = sql + " res:" + resource
                        elif query[i] == 'dbo/dbp:':
                            if query[i+1] == 'res:' or query[i-1] == 'res:':
                                sql = sql + " " + prop1.propertyType + ":" + prop1.property
                            else:
                                sql = sql + " " + propLast.propertyType + ":" + propLast.property
                        else:
                            sql = sql + " " + query[i]
                    sqls.append(sql)

    if query[2] == 3:
        for i, resource in enumerate(resourceList):
            for prop1 in propertyList[i]:
                for propLast1 in propertyList[len(resourceList)]:
                    for propLast2 in propertyList[len(resourceList)]:
                        sql = ''
                        dboDbpCount = 0
                        for i in range(3, 20, 1):
                            if query[i] == 'res:':
                                sql = sql + " res:" + resource
                            elif query[i] == 'dbo/dbp:':
                                if query[i+1] == 'res:' or query[i-1] == 'res:':
                                    sql = sql + " " + prop1.propertyType + ":" + prop1.property
                                else:
                                    if dboDbpCount == 0:
                                        sql = sql + " " + propLast1.propertyType + ":" + propLast1.property
                                        dboDbpCount = dboDbpCount + 1
                                    elif dboDbpCount == 1:
                                        sql = sql + " " + propLast2.propertyType + ":" + propLast2.property
                            else:
                                sql = sql + " " + query[i]
                        sqls.append(sql)

    if query[2] == 4:
        for i, resource in enumerate(resourceList):
            for prop1 in propertyList[i]:
                for propLast1 in propertyList[len(resourceList)]:
                    for propLast2 in propertyList[len(resourceList)]:
                        for propLast3 in propertyList[len(resourceList)]:
                            sql = ''
                            dboDbpCount = 0
                            for i in range(3, 20, 1):
                                if query[i] == 'res:':
                                    sql = sql + " res:" + resource
                                elif query[i] == 'dbo/dbp:':
                                    if query[i+1] == 'res:' or query[i-1] == 'res:':
                                        sql = sql + " " + prop1.propertyType + ":" + prop1.property
                                    else:
                                        if dboDbpCount == 0:
                                            sql = sql + " " + propLast1.propertyType + ":" + propLast1.property
                                            dboDbpCount = dboDbpCount + 1
                                        elif dboDbpCount == 1:
                                            sql = sql + " " + propLast2.propertyType + ":" + propLast2.property
                                            dboDbpCount = dboDbpCount + 1
                                        elif dboDbpCount == 2:
                                            sql = sql + " " + propLast3.propertyType + ":" + propLast3.property
                                else:
                                    sql = sql + " " + query[i]
                            sqls.append(sql)

    return list(property_selection.removeDuplicates(sqls))


def formateResourceAndPropertyData(propertyList, resourceList):
    for i in range(0, len(resourceList)):
        resource = resourceList[i]
        resource = resource.replace(",", "\,")
        resource = resource.replace(".", "\.")
        resource = resource.replace("+", "\+")
        resource = resource.replace("(", "\(")
        resource = resource.replace(")", "\)")
        resourceList[i] = resource

    for i in range(0, len(propertyList)):
        for j in range(0, len(propertyList[i])):
            # c =
            propertyList[i][j].property = propertyList[i][j].property.replace("/", "\/")
            # propertyList[i][j] = b


def getQueryResult(propertyList, resourceList, queryIDs):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    answerArray = []

    queries = mysql_operations.getAllSparqlQuery(queryIDs)
    sqls = []

    formateResourceAndPropertyData(propertyList, resourceList)

    for query in queries:
        noOfRes = query[1]

        if noOfRes == 0:
            sqls.append(makeZeroResSql(propertyList, query))
        elif noOfRes == 1:
            sqls.append(makeOneResSql(propertyList, resourceList, query))

    for sqlsRow in sqls:
        for sql in sqlsRow:
            print(constant.prefix + sql)
            sparql.setQuery(constant.prefix + sql)
            try:
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                if query[0] in (20, 21):
                    answerArray.append(results['boolean'])
                else:
                    tempResultArray = []
                    for result in results["results"]["bindings"]:
                        tempResultArray.append(result["label"]["value"])
                    answerArray.append(tempResultArray)
            except:
                pass

    return answerArray
