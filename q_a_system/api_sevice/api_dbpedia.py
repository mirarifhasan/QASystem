from SPARQLWrapper import SPARQLWrapper, JSON
from q_a_system.global_pack import strings


def getQueryResult(propertyList, resourceList):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    answer_array = []

    for property in propertyList:
        resource = resourceList[0]

        sql = """
            SELECT distinct ?label
            WHERE { res:""" + resource + """ """ + property.propertyType + """:""" + property.property + """ ?label }
        """
        print(strings.prefix + sql)
        sparql.setQuery(strings.prefix + sql)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        tempResultArray = []
        for result in results["results"]["bindings"]:
            tempResultArray.append(result["label"]["value"])

        answer_array.append(tempResultArray)

    return answer_array