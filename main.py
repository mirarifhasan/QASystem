from q_a_system.spacy_play import name_entity, resource_name, parts_of_speech,keyword_extraction
from q_a_system.input_output import input
from q_a_system.api_sevice import api_dbpedia

#question = input.getUserQuestion()
question = 'When was Obama born?'

nameEntityArray = name_entity.getNameEntity(question)

#print(nameEntityArray)
#parts_of_speech.printAllWordDetails(question)
keyword_extraction.printAllKeywords(question)

if len(nameEntityArray) > 0:
    resourceList = resource_name.getResourceName(nameEntityArray)
    print(resourceList)

api_dbpedia.getQueryResult(resourceList[0])