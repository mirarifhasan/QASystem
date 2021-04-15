from itertools import chain

from q_a_system.api_sevice import api_dbpedia, mysql_operations
from q_a_system.global_pack import constant
from q_a_system.Logging import saveLogs
import threading
from q_a_system.method import byAutomation, byDataDictionary, lookup_things
from q_a_system.spacy_play import name_entity, resource_name, answer_type_extraction, answer_validation, \
    question_type_extraction
from q_a_system.spacy_play.property_selection import getActualProperty, addAdditionalSet
from q_a_system.web_scrape.propertyScrape import getPageProperties

import pandas as pd
import datetime

# questions = input.getUserQuestion()

questions = constant.quesGSheet.col_values(1)[1:]

# questions = ['Who is the son of Sonny and Cher? ']

# questions = [
#     'Which films did Stanley Kubrick direct?', #Stanley Kubrick filmography (partially)
#     'In which time zone is Rome?', # Zones of Rome
#     'Which actors play in Big Bang Theory?', #Kevin Sussman, Jim Parsons, Kaley Cuoco, Sara Gilbert, Kunal Nayyar, Laura Spencer (actress), Simon Helberg, Johnny Galecki, Mayim Bialik, Melissa Rauch
#     'Which companies produce hovercrafts?', # m.013xl3, Hovercraft, 4036570-0, 氣墊船, হোভারক্রাফ্ট, Luchtkessenreau, Лебдјелица,....
#     'In which ancient empire could you pay with cocoa beans?', # Ghanaian cedi, Euro, West African CFA franc
#     'Which space probes were sent into orbit around the sun?', # Earth?oldid=986561235&ns=0(partially)
#     'On which day is Columbus day?', # October
#     'To which party does the mayor of Paris belong?', #Paris Belongs to Us, m.04f02jr, پاریس از آن ماست, 12PyxB, パリはわれらのもの, Paris gehört uns, Paris nous appartient, Paris nous appartient, Q25513, Parigi ci appartiene
#     'Which country was Bill Gates born in?', # Bremerton, Washington
#     'In which countries do people speak Japanese?', # Japan, Japan
#     'Which rivers flow into the North Sea?', # Baltic Sea, Humber, Scheldt, Rhine, River Dee, Aberdeenshire, River Don....
#     'Which movies starboth Liz Taylor and Richard Burton?', # Love Is Better Than Ever, Under Milk Wood (1972 film), Boom! (film), Doctor Faustus (1967 film),
#     'Which electronics companies were founded in Beijing?', # Chen Jining, Cai Qi, Ji Lin, Li Wei (PRC politician)
#     'Which Indiancompany has the most employees?', #  https://global.dbpedia.org/id/5EMPt or No Answer
#     'Which countries have more than ten volcanoes?', # Decade Volcanoes, m.05czx5, 十年火山, Декадни вулкани, Vulcões da Década, Декадные вулканы, Decade Volcanoes,
#     'In which city was the president of Montenegro born?' # SR Montenegro, Cetinje, Yugoslavia, Nikšić, Socialist Federal Republic of Yugoslavia, Socialist Republic of Montenegro
#     # 'Which writers studied in Istanbul?'
# ]

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
    nameEntityList = list(dict.fromkeys(nameEntityList))
    print(str([x.text for x in nameEntityList]))


    print("Step 2: Keywords finding")
    # finding keyword list by build in services
    keywordListByAM = byAutomation.findKeywordByAutomation(question)
    # finding keyword list by DataDictionary approach
    keywordListByDD = byDataDictionary.find_keyword_by_dataDictionary(question)

    keywordList = list(chain.from_iterable([keywordListByDD, keywordListByAM]))
    print(keywordList)


    resourceList = []
    stringList = []
    if len(nameEntityList) > 0:
        print("Step 3: Resource Name finding")
        if flagResFromGoogleSearch == True:
            # Making string
            stringList = lookup_things.getResKeywordString(nameEntityList, keywordList)
            print(f"string to pass: {stringList}")
            # Google search
            resourceList = resource_name.getResourceNameByGoogleSearch(stringList)
        else:
            resourceList = resource_name.getResourceName(nameEntityList)
            flagResFromGoogleSearch = True

        print(f"resource list: {resourceList}")

    if len(resourceList) == 0: # for having 429 error
        resourceList = resource_name.getResourceNameWithString(stringList)
        print(f"resource list: {resourceList}")


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


    if 'answer' in vars():
        threading.Thread(target=saveLogs.saveOneLog, args=([question, str([x.text for x in nameEntityList]), str(stringList), str(resourceList), str(keywordList), log_var_property_list, answer], )).start()
    else:
        threading.Thread(target=saveLogs.saveOneLog, args=([question, str([x.text for x in nameEntityList]), str(stringList), str(resourceList), str(keywordList), log_var_property_list, None], )).start()
    print('\n\n\n')

