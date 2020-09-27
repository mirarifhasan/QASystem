from q_a_system.method import byAutomation
from q_a_system.spacy_play import name_entity, resource_name, parts_of_speech, keyword_extraction, \
    anwer_type_extraction, answer_validation, question_type_extraction
from q_a_system.input_output import input
from q_a_system.api_sevice import api_dbpedia, mysql_operations
from q_a_system.spacy_play.keyword_extraction import removeNounChunks
from q_a_system.spacy_play.property_selection import getActualProperty
from q_a_system.web_scrape.propertyScrape import getPageProperties
import datetime

# question = input.getUserQuestion()
question = 'When was obama born?'
# question = 'Who is the president of Eritrea?'

# byAutomation.byAutomation(question)

print("Step 1: Name Entity finding")
nameEntityList = name_entity.getNameEntity(question)
print(nameEntityList)

if len(nameEntityList) > 0:
    print("Step 2: Resource Name finding")
    resourceList = resource_name.getResourceName(nameEntityList)
    print(resourceList)

    if len(resourceList) > 0:
        print("Step 3: Keywords finding")
        # finding keyword list by build in services
        keywordList = byAutomation.findKeywordByAutomation(question)
        print(keywordList)

        # finding keyword list by DataDictionary approach
        # call 'byDataDictionary.{function name with parameter}'
        # keywordListByDD = byDataDictionary.find_keyword_by_automation(question)
        # print(f'keywordListByDD : {keywordListByDD}')
        # DataDictionary approach calling END here

        print("Step 4: Property finding")
        propertyList = getPageProperties(resourceList[0])
        propertyList = getActualProperty(keywordList, propertyList)
        print(propertyList)

        if len(propertyList) > 0:
            print("Step 5.0.1: Get Sparql Query IDs")
            questionType = question_type_extraction.findQuestionType(question)
            queryIDs = mysql_operations.findSparqlQueryID(questionType)

            print("Step 5: All possible answer finding")
            answerArray = api_dbpedia.getQueryResult(propertyList, resourceList, queryIDs)
            print(answerArray)

            print("Step 6: Answer type extraction")
            questionType = anwer_type_extraction.printAnswerType(question, keywordList)
            print("Expected Answer Type : " + questionType)

            # type = anwer_type_extraction.printAnswerType(question)

            print("Step 7: Answer type validation")
            answer = answer_validation.answerValidation(answerArray, questionType)
            print("Actual Answer: " + answer)

        else:
            print("No property found! Can't go forward without property")
