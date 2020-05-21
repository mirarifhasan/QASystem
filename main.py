from q_a_system.spacy_play import name_entity, resource_name, parts_of_speech,keyword_extraction
from q_a_system.input_output import input
from q_a_system.api_sevice import api_dbpedia
from q_a_system.spacy_play.keyword_extraction import removeNounChunks, getActualProperty
from q_a_system.web_scrape.propertyScrape import getPageProperties

# question = input.getUserQuestion()
question = 'When was Obama born?'


nameEntityList = name_entity.getNameEntity(question)

if len(nameEntityList) > 0:
    resourceList = resource_name.getResourceName(nameEntityList)

    if len(resourceList) > 0:
        keywordList = keyword_extraction.getAllKeywords(question)
        keywordList = removeNounChunks(question, keywordList)

        propertyList = getPageProperties(resourceList[0])

        propertyListIndex = getActualProperty(keywordList, propertyList)


        api_dbpedia.getQueryResult(resourceList[0])