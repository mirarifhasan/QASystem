from SPARQLWrapper import SPARQLWrapper, JSON

#resource = "Donald_Trump"
def getQueryResult(resource):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo:<http://dbpedia.org/ontology/>
        PREFIX res:<http://dbpedia.org/resource/>
        SELECT ?label
        WHERE { res:"""+resource+""" dbo:birthDate ?label }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print(result["label"]["value"])