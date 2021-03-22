from q_a_system.api_sevice import api_dbpedia, mysql_operations
from q_a_system.method import byAutomation, byDataDictionary, lookup_things
from q_a_system.spacy_play import name_entity, resource_name, answer_type_extraction, answer_validation, \
    question_type_extraction
from q_a_system.spacy_play.property_selection import getActualProperty, addAdditionalSet
from q_a_system.web_scrape.propertyScrape import getPageProperties

import pandas as pd
import datetime


# questions = input.getUserQuestion()
# questions=['How many movies did Park Chan-wook direct?','How many headquarters are in Dhaka?']

input_file_directory = "Code Behaviours - QLD6_SingleResource.csv"
output_file_directory = "output log.csv"
input_file = pd.read_csv(input_file_directory, encoding='cp1252')
questions = input_file["Question"].tolist()

log_named_entity_list = []
log_resource_list = []
log_keyword_list = []
log_property_list = []
log_sql_list = []
log_all_answer_list = []
log_answer_list = []
log_question_type_list = []


for question in questions:

    print(question)

    print("\nStep 1: Name Entity finding")
    nameEntityList = name_entity.getNameEntity(question)
    log_var_named_entity_list = ''
    for nameEntity in nameEntityList:
        print(nameEntity.text)
        log_var_named_entity_list = log_var_named_entity_list + nameEntity.text + ', '
    log_named_entity_list.append(log_var_named_entity_list)


    print("Step 3: Keywords finding")
    # finding keyword list by build in services
    keywordListByAM = byAutomation.findKeywordByAutomation(question)
    print(keywordListByAM)

    # finding keyword list by DataDictionary approach
    keywordListByDD = byDataDictionary.find_keyword_by_dataDictionary(question)
    print(keywordListByDD)

    keywordList = []
    for i in keywordListByDD:
        keywordList.append(i)
    for i in keywordListByAM:
        keywordList.append(i)

    log_keyword_list.append(keywordList)


    if len(nameEntityList) > 0:
        print("Step 2: Resource Name finding")
        # Making string
        stringList = lookup_things.getResKeywordString(nameEntityList, keywordList)
        # Google search
        resourceList = resource_name.getResourceNameByGoogleSearch(stringList)
        # resourceList = resource_name.getResourceName(nameEntityList)
        print(resourceList)
        log_var_resource_list = ''
        for i in resourceList:
            log_var_resource_list = log_var_resource_list + i + ', '
        log_resource_list.append(log_var_resource_list)


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
    log_property_list.append(log_var_property_list)

    if hasProperty:
        print("Step 5.0.1: Get Sparql Query IDs")
        questionType = question_type_extraction.findQuestionType(question)
        queryIDs = mysql_operations.findSparqlQueryID(questionType, question)

        print("Step 5: All possible answer finding")
        answerArray, sqls = api_dbpedia.getQueryResult(propertyList, resourceList, queryIDs)
        print(answerArray)

        print("Step 6: Answer type extraction")
        questionType = answer_type_extraction.printAnswerType(question, keywordList)
        print("Expected Answer Type : " + questionType)

        print("Step 7: Answer type validation")
        answer = answer_validation.answerValidation(answerArray, questionType)
        print("Actual Answer: " + answer)

        log_sql_list.append(sqls)
        log_all_answer_list.append(answerArray)
        log_answer_list.append(answer)
        log_question_type_list.append(questionType)

    else:
        print("No property found! Can't go forward without property")

    print('\n\n\n')



# writing the logs in csv file
output_file = pd.DataFrame(
    {
        'Questions': questions,
        'Name Entity': log_named_entity_list,
        'Resources': log_resource_list,
        'Keyword': log_keyword_list,
        'Property': log_property_list,
        'Answer Array': log_all_answer_list,
        'Answer Type': log_question_type_list,
        'Answer': log_answer_list,
        'SQL': log_sql_list
    }
)
output_file.to_csv(output_file_directory)
