from q_a_system.api_sevice import api_dbpedia, mysql_operations
from q_a_system.method import byAutomation, byDataDictionary
from q_a_system.spacy_play import name_entity, resource_name, answer_type_extraction, answer_validation, \
    question_type_extraction
from q_a_system.spacy_play.property_selection import getActualProperty
from q_a_system.web_scrape.propertyScrape import getPageProperties

# question = input.getUserQuestion()
#questions = ['When did the Dodo become extinct?', 'When did the Boston Tea Party take place?']
#questions = ['When was obama born?', 'When did princess Diana die?', 'When did Operation Overlord commence?', 'When did the Dodo become extinct?', 'When did Boris Becker end his active career?', 'When did the Boston Tea Party take place?']
#questions = ['Where do the Red Sox play?', 'Where is Syngman Rnhee buried?', 'Where does Piccadilly start?']
#questions=['Whom did Lance Bass marry? ', 'Whom did Obama marry?']
#questions = ['Who is president of Eritrea?','Who was doctoral supervisor of Albert Einstein?','Who wrote the song Hotel California?','Who was on the Apollo 11 mission?', 'Who wrote Harry Potter?','Who are developers of DBpedia?']
#questions = ['Show me all books in Asimov’s Foundation series.','Who developed Slack? ','Who is mayor of Paris?']
questions=['Who created Family Guy?', 'Who does the voice of Bart Simpson?' ]
#questions= ['How many moons does Mars have?','How much did the Lego Movie cost? ','How many people live in Poland?']
for question in questions:
    print(question)
    print("Step 1: Name Entity finding")
    nameEntityList = name_entity.getNameEntity(question)
    for nameEntity in nameEntityList:
        print(nameEntity.text)

    if len(nameEntityList) > 0:
        print("Step 2: Resource Name finding")
        resourceList = resource_name.getResourceName(nameEntityList)
        print(resourceList)

        if len(resourceList) > 0:
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



            print("Step 4: Property finding")
            propertyList = getPageProperties(resourceList[0])
            propertyList = getActualProperty(keywordList, propertyList, keywordListByDD)

            for prop in propertyList:
                print(prop.label)

            if len(propertyList) > 0:
                print("Step 5.0.1: Get Sparql Query IDs")
                questionType = question_type_extraction.findQuestionType(question)
                queryIDs = mysql_operations.findSparqlQueryID(questionType)

                print("Step 5: All possible answer finding")
                answerArray = api_dbpedia.getQueryResult(propertyList, resourceList, queryIDs)
                print(answerArray)

                print("Step 6: Answer type extraction")
                questionType = answer_type_extraction.printAnswerType(question, keywordList)
                print("Expected Answer Type : " + questionType)

                print("Step 7: Answer type validation")
                answer = answer_validation.answerValidation(answerArray, questionType)
                print("Actual Answer: " + answer)

            else:
                print("No property found! Can't go forward without property")

    print('\n\n\n')
