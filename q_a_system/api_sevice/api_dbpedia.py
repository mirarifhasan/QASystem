from SPARQLWrapper import SPARQLWrapper, JSON
from q_a_system.global_pack import constant


def getQueryResult(propertyList, resourceList):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    answerArray = []

    for property in propertyList:
        resource = resourceList[0]

        sql = """
            SELECT distinct ?label
            WHERE { res:""" + resource + """ """ + property.propertyType + """:""" + property.property + """ ?label }
        """

        print(constant.prefix + sql)
        sparql.setQuery(constant.prefix + sql)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        tempResultArray = []
        for result in results["results"]["bindings"]:
            tempResultArray.append(result["label"]["value"])

        answerArray.append(tempResultArray)

    return answerArray
