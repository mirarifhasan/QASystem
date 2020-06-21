import spacy


# lang = 'en_vectors_web_lg'
lang = 'en_core_web_lg'
# lang = 'en_core_web_md'
# lang = 'en_core_web_sm'
# lang = 'en'

minSimilarity = 0.55

nlp = spacy.load(lang)

prefix = """ PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dbo:<http://dbpedia.org/ontology/>
            PREFIX res:<http://dbpedia.org/resource/> """