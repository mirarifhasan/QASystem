from q_a_system.spacy_play import name_entity, resource_name, parts_of_speech,keyword_extraction,anwer_type_extraction, answer_validation
from q_a_system.input_output import input
from q_a_system.api_sevice import api_dbpedia
from q_a_system.spacy_play.keyword_extraction import removeNounChunks, getActualProperty
from q_a_system.web_scrape.propertyScrape import getPageProperties

# question = input.getUserQuestion()
question = 'When was obama born?'

print("Step 1: Name Entity finding")
nameEntityList = name_entity.getNameEntity(question)
print(nameEntityList)

if len(nameEntityList) > 0:
    print("Step 2: Resource Name finding")
    resourceList = resource_name.getResourceName(nameEntityList)
    print(resourceList)

    if len(resourceList) > 0:
        print("Step 3: Keywords finding")
        keywordListTemp = keyword_extraction.getAllKeywords(question)
        keywordList = removeNounChunks(question, keywordListTemp)
        print(keywordList)

        print("Step 4: Property finding")
        propertyList = getPageProperties(resourceList[0])
        propertyList = getActualProperty(keywordList, propertyList)
        print(propertyList)

        print("Step 5: All possible answer finding")
        answerArray = api_dbpedia.getQueryResult(propertyList, resourceList)
        print(answerArray)

        print("Step 6: Answer type extraction")
        type = anwer_type_extraction.printAnswerType(question, keywordListTemp)
        print("Expected Answer Type : " + type)

        print("Step 7: Answer type validation")
        answer = answer_validation.answerValidation(answerArray,type)
        print("Actual Answer  : " + answer)
