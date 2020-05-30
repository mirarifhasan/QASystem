from SPARQLWrapper import SPARQLWrapper, JSON
from q_a_system.global_pack import strings
answer_array=[]
#resource = "Donald_Trump"
def getQueryResult(propertyList, resourceList):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    for property in propertyList:
        resource = resourceList[0]

        sql = """
            SELECT ?label
            WHERE { res:""" + resource + """ """ + property.propertyType + """:""" + property.property + """ ?label }
        """
        # print(strings.prefix + sql)
        sparql.setQuery(strings.prefix + sql)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            answer_array.append(result["label"]["value"])

    return answer_array