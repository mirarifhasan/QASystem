from q_a_system.api_sevice import api_dbpedia, mysql_operations
from q_a_system.method import byAutomation, byDataDictionary
from q_a_system.spacy_play import name_entity, resource_name, answer_type_extraction, answer_validation, question_type_extraction
from q_a_system.spacy_play.property_selection import getActualProperty, addAdditionalSet
from q_a_system.web_scrape.propertyScrape import getPageProperties


#questions = input.getUserQuestion()
#questions = ['When did the Boston Tea Party take place?','When does the ottoman state founded?']
#questions = ['When did the Dodo become extinct?', 'When was obama born?', 'When did princess Diana die?', 'When did Operation Overlord commence?', 'When did the Dodo become extinct?', 'When did Boris Becker end his active career?', 'When did the Boston Tea Party take place?']
#questions = ['Where do the Red Sox play?', 'Where is Syngman Rnhee buried?', 'Where does Piccadilly start?']
#questions=['Whom did Lance Bass marry? ', 'Whom did Obama marry?']
#questions = ['Who is president of Eritrea?','Who was doctoral supervisor of Albert Einstein?','Who wrote the song Hotel California?','Who was on the Apollo 11 mission?', 'Who wrote Harry Potter?','Who are developers of DBpedia?', 'Who created Family Guy?', 'Who does the voice of Bart Simpson?']
#questions=['Who played Gus Fring in Breaking Bad?','Who composed soundtrack for Cameron’s Titanic?','Who is mayor of Paris?' ]
#questions=['Who discovered Ceres?','Who is the host of the BBC Wildlife Specials?','Who wrote the Game of Thrones theme?']
#questions=['Who developed Slack?','Who was Vincent van Gogh inspired by?']
#questions=['Who is the president of Eritrea?','Who is the mayor of Paris?','Who are the developers of DBpedia']
#questions=['What is in a chocolate chip cookie? ','What is the atmosphere of the Moon composed of?','What is the capital of Cameroon? ','What country is Sitecore from?']
#questions=['What is full name of Prince Charles?','What is Batman’s real name?']

##=====================unprocessed
#questions = ['Show me all books in Asimov’s Foundation series.']
#questions= ['How many moons does Mars have?','How many people live in Poland?','How much did the Lego Movie cost?','How many movies did Park Chan-wook direct?' ,'How many calories does a baguette have?']
#questions=[ 'How many emperors did China have?', 'How did Michael Jackson die?']


#questions=[  'What languages do they speak in Pakistan?','What is Elon Musk famous for?','What is Batman’s real name?','What form of government does Russia have?','What kind of music did Lou Reed play?']
#questions=['What color expresses loyalty?','What are the five boroughs of New York?','What are the zodiac signs?']

#questions=['Which actors play in Big Bang Theory?', 'In which time zone is Rome?']
#questions=['On which day is Columbus Day?', 'Who played Gus Fring in Breaking Bad?']

#questions=['What languages do they speak in Pakistan?','What form of government does Russia have?']
#questions=['Show me all U.S. states']

#' Did Elvis Presley have children?'
#questions=['Does Neymar play for Real Madrid?', 'Did Kaurismäki ever win the Grand Prix at Cannes?' ]
#questions=['What form of government does Russia have?','Which films did Stanley Kubrick direct?','Which companies produce hovercrafts?']
#questions=[ 'In which ancient empire could you pay with cocoa beans?']
#questions=['Which space probes were sent into orbit around the sun?']
#questions=['What movies does Jesse Eisenberg play in?','Who is the king of the Netherlands?']
#,'What form of government does Russia have?','What kind of music did Lou Reed play?','What are the names of the Teenage Mutant Ninja Turtles?','What are the zodiac signs?']
#'What is the capital of Cameroon? ','What country is Sitecore from?','What is in a chocolate chip cookie?','What is the atmosphere of the Moon composed of?','How many emperors did China have?','How much did the Lego Movie cost?','Whom did Lance Bass marry?','How many movies did Park Chan-wook direct?','How many goals did Pelé score?','How many people live in Poland?','How many moons does Mars have?',,'How many calories does a baguette have?'
questions=['On which day is Columbus day?']


######### our dataset
#"Whose father is Sheikh Mujibur Rahman?"
#, 'What is the official language of turkey ?','What is the full name of turkey?', What is the species of royal Bengal tiger?', 'What is the nick name of Ahsanullah University of Science and Technology?','What is the currency code of Turkey?', "What is the birth name of  Nina Pillard?",'How many goals given by Maradona in total?','How many runs scored by Shakib Al Hasan in total?','What is the bowling average of Shakib Al Hasan?','What is the top score of Shakib Al Hasan?',,'How many wickets are taken by Shakib Al Hasan at maximum?','What is the batting average of  Shakib Al Hasan?'
# 'Where  is Ahsanullah University of Science and Technology located?','When was Maynamati War Cemetery  established ?','Where was Shakib Al Hasan born?' 'Where  was Maynamati War Cemetery established ?','Where was Kazi Nazrul Islam born?'
#'Show me all books in Asimov’s Foundation series.','Did Elvis Presley have children?','Where do the Red Sox play?','Where is Syngman Rhee buried?','Who was on the Apollo 11 mission?','Who wrote the song Hotel California?','Where does Piccadilly start?'
#questions=['When was obama born?']


#questions= ['When was 7-up invented?', 'When was Anne Wojcicki born ?','When does the ottoman state founded?','When does the ottoman state end?','When was Comilla city established ?','When was Maynamati War Cemetery  established ?','When was Ahsanullah University of Science and Technology established ?','When was Nina Pilard born?']
# 'Show me the universities of Bangladesh ?', 'Show the broadcast channels of Bangladesh?','How many 100s/50s  has got Sakib Al Hasan  in his carier?'
#questions=['How many matches Sakib Al Hasan played?',How many undergraduates study in  Ahsanullah University of Science and Technology?','How has Kazi Nazrul Islam been influenced in writing rebel poem?']
#questions=['How many movies did Park Chan-wook direct?','How many headquarters are in Dhaka?']

for question in questions:
    print(question)

    print("\nStep 1: Name Entity finding")
    nameEntityList = name_entity.getNameEntity(question)
    for nameEntity in nameEntityList:
        print(nameEntity.text)

    if len(nameEntityList) > 0:
        print("Step 2: Resource Name finding")
        resourceList = resource_name.getResourceName(nameEntityList)
        print(resourceList)

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

    if len(resourceList) > 0:
        print("Step 4: Property finding")
        propertyList = getPageProperties(resourceList)
        propertyList = getActualProperty(keywordList, propertyList)
        propertyList.append(addAdditionalSet(keywordListByDD))

    hasProperty = False
    for propertyListSingle in propertyList:
        for prop in propertyListSingle:
            hasProperty = True
            print(prop.label)

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

    else:
        print("No property found! Can't go forward without property")

    print('\n\n\n')
