from q_a_system.api_sevice import db_connect


def findSparqlQueryID(whWord, question):
    queryIDs = []

    queryIDs = findIfAggregate(question)
    if len(queryIDs) > 0:
        return queryIDs

    cursor = db_connect.connection.cursor()
    try:
        sql = "SELECT sparql_id FROM sparql_wh WHERE wh_id = ( SELECT wh_id FROM wh_word WHERE wh_word_name = '" + whWord + "' )"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            queryIDs.append(row[0])
    except:
        print("Something else went wrong")

    cursor.close()
    return queryIDs


def findIfAggregate(question):
    queryIDs = []
    questionWords = question.split(' ')
    questionWords[-1] = questionWords[-1].replace("?", "")

    for word in questionWords:
        if word in ['top', 'maximum']:
            queryIDs = [22]
        elif word in ['total']:
            queryIDs = [23]
        elif word in ['average']:
            queryIDs = [24]

    return queryIDs


def getAllSparqlQuery(queryIDs):
    sql = "SELECT * FROM sparql_query WHERE query_id IN ( "
    temp = 0
    for queryID in queryIDs:
        sql = sql + str(queryID)
        if temp != len(queryIDs) - 1:
            sql = sql + ", "
            temp = temp + 1
    sql = sql + " )"

    cursor = db_connect.connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()

    return results


def findResource(nameEntity):
    sql = "SELECT * FROM resource_dictionary WHERE name_entity = '" + nameEntity + "'"
    cursor = db_connect.connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()

    return results
