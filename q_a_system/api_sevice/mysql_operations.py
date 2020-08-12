from q_a_system.api_sevice import db_connect

def findSparqlQueryID(whWord):
    queryIDs = []
    wordID = 0

    cursor = db_connect.connection.cursor()
    try:
        cursor.execute("SELECT wh_id FROM wh_word WHERE wh_word_name = '" + whWord + "'")
        results = cursor.fetchall()
        for row in results:
            wordID = row[0]
    except:
        print("Something else went wrong")

    try:
        cursor.execute("SELECT sparql_id FROM sparql_wh WHERE wh_id = " + str(wordID))
        results = cursor.fetchall()
        for row in results:
            queryIDs.append(row[0])
    except:
        print("Something else went wrong")

    cursor.close()
    return queryIDs

def getAllSparqlQuery(queryIDs):

    sql = "SELECT * FROM sparql_query WHERE query_id IN ( "
    temp = 0
    for queryID in queryIDs:
        sql = sql + str(queryID)
        if temp != len(queryIDs)-1:
            sql = sql + ", "
            temp = temp + 1
    sql = sql + " )"

    cursor = db_connect.connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()

    return results


print(getAllSparqlQuery([1, 2]))