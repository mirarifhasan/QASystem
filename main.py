import time
from itertools import chain

from q_a_system.api_sevice import api_dbpedia, mysql_operations
from q_a_system.global_pack import constant
from q_a_system.Logging import logWorks
import threading
from q_a_system.method import byAutomation, byDataDictionary, lookup_things
from q_a_system.spacy_play import name_entity, resource_name, answer_type_extraction, answer_validation, \
    question_type_extraction
from q_a_system.spacy_play.property_selection import getActualProperty, addAdditionalSet
from q_a_system.web_scrape.propertyScrape import getPageProperties

import pandas as pd
import datetime

# questions = input.getUserQuestion()

questions, expectedResource, expectedProperty, expectedAnswer = logWorks.getInputQ()

log_question_list = []

ques_count = 0
flagResFromGoogleSearch = True

questionIndex = 0
while questionIndex < len(questions):

    question = questions[questionIndex]
    log_question_list.append(question)

    print(f"\n\n#{ques_count}")
    print(question)
    ques_count = ques_count + 1


    print("\nStep 1: Name Entity finding")
    nameEntityList = name_entity.getNameEntity(question)
    print(str([x.text for x in nameEntityList]))


    print("Step 2: Keywords finding")
    # finding keyword list by build in services
    keywordListByAM = byAutomation.findKeywordByAutomation(question)
    # finding keyword list by DataDictionary approach
    keywordListByDD = byDataDictionary.find_keyword_by_dataDictionary(question.replace("\'s", ""))

    keywordList = list(chain.from_iterable([keywordListByDD, keywordListByAM]))
    print(keywordList)


    resourceList = []
    stringList = []
    if len(nameEntityList) > 0:
        print("Step 3: Resource Name finding")
        if flagResFromGoogleSearch == True:
            # Making string
            # stringList = lookup_things.getResKeywordString(nameEntityList, keywordList)
            # print(f"string to pass: {stringList}")
            # Google search
            resourceList = resource_name.getResourceNameByGoogleSearch([ne.text for ne in nameEntityList])
            print(f"resource list (google search): {resourceList}")
        else:
            resourceList = resource_name.getResourceName(nameEntityList)
            print(f"resource list (wiki search): {resourceList}")
            flagResFromGoogleSearch = True


    # if len(resourceList) == 0: # for having 429 error
    stringList = lookup_things.getResKeywordString(nameEntityList, keywordList)
    print(f"string to pass: {stringList}")

    # resourceList = resource_name.getResourceNameWithString(stringList)
    resourceList = list(dict.fromkeys(list(chain.from_iterable([resource_name.getResourceNameWithString(stringList), resourceList]))))
    print(f"resource list (google + string): {resourceList}")


    propertyList = [[]]
    if len(resourceList) > 0:
        print("Step 4: Property finding")
        propertyList = getPageProperties(resourceList)
        propertyList = getActualProperty(keywordList, propertyList)
    propertyList.append(addAdditionalSet(keywordListByDD))

    hasProperty = False
    temp = -1
    log_var_property_list = ''
    for propertyListSingle in propertyList:
        temp = temp + 1
        for prop in propertyListSingle:
            hasProperty = True
            print(prop.label)
            log_var_property_list = log_var_property_list + '(' + str(temp) + prop.property + '-' + str(
                prop.similarity) + '), '
    print(f"property list: {log_var_property_list}")


    if hasProperty:
        print("Step 5.0.1: Get Sparql Query IDs")
        questionType = question_type_extraction.findQuestionType(question)
        queryIDs = mysql_operations.findSparqlQueryID(questionType, question)

        print("Step 5: All possible answer finding")
        # answerArray, sqls = api_dbpedia.getQueryResult(propertyList, resourceList, queryIDs)
        answerArray, sqls = api_dbpedia.get_query_result(propertyList, resourceList, queryIDs, questionType)
        print(answerArray)

        print("Step 6: Answer type extraction")
        questionType = answer_type_extraction.printAnswerType(question, keywordList)
        print("Expected Answer Type : " + questionType)

        print("Step 7: Answer type validation")
        answer = answer_validation.answerValidation(answerArray, questionType)
        print("Actual Answer: " + answer)

        if answer == "No answer" and log_question_list[len(log_question_list) - 1] != log_question_list[len(log_question_list) - 2]:
            flagResFromGoogleSearch = False
            continue
        else:
            questionIndex = questionIndex + 1

    else:
        print("No property found! Can't go forward without property")
        if log_question_list[len(log_question_list) - 1] != log_question_list[len(log_question_list) - 2]:
            flagResFromGoogleSearch = False
            continue
        else:
            questionIndex = questionIndex + 1


    if 'answer' in vars() and 'sqls' in vars():
        if len(sqls) > 200:
            sqls = sqls[:200]
        threading.Thread(target=logWorks.saveOneLog, args=([str(datetime.datetime.now()), question, str([x.text for x in nameEntityList]), str(stringList), str(resourceList), expectedResource[questionIndex-1], str(keywordList), log_var_property_list, expectedProperty[questionIndex-1], answer, expectedAnswer[questionIndex-1], "\n".join(sqls)],)).start()
    else:
        threading.Thread(target=logWorks.saveOneLog, args=([str(datetime.datetime.now()), question, str([x.text for x in nameEntityList]), str(stringList), str(resourceList), expectedResource[questionIndex-1], str(keywordList), log_var_property_list, expectedProperty[questionIndex-1], None, expectedAnswer[questionIndex-1]], None,)).start()
    print('\n\n\n')

