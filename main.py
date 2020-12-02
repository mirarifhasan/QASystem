from q_a_system.api_sevice import api_dbpedia, mysql_operations
from q_a_system.method import byAutomation, byDataDictionary
from q_a_system.spacy_play import name_entity, resource_name, answer_type_extraction, answer_validation, \
    question_type_extraction
from q_a_system.spacy_play.property_selection import getActualProperty
from q_a_system.web_scrape.propertyScrape import getPageProperties
import warnings
import time

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

# questions = input.getUserQuestion()
# questions = ['When did the Boston Tea Party take place?','When does the ottoman state founded?']
# questions = ['When did the Dodo become extinct?', 'When was obama born?', 'When did princess Diana die?', 'When did Operation Overlord commence?', 'When did the Dodo become extinct?', 'When did Boris Becker end his active career?', 'When did the Boston Tea Party take place?']
# questions = ['Where do the Red Sox play?', 'Where is Syngman Rnhee buried?', 'Where does Piccadilly start?']
# questions=['Whom did Lance Bass marry? ', 'Whom did Obama marry?']
# questions = ['Who is president of Eritrea?','Who was doctoral supervisor of Albert Einstein?','Who wrote the song Hotel California?','Who was on the Apollo 11 mission?', 'Who wrote Harry Potter?','Who are developers of DBpedia?', 'Who created Family Guy?', 'Who does the voice of Bart Simpson?']
# questions=['Who played Gus Fring in Breaking Bad?','Who composed soundtrack for Cameron’s Titanic?','Who is mayor of Paris?' ]
# questions=['Who discovered Ceres?','Who is the host of the BBC Wildlife Specials?','Who wrote the Game of Thrones theme?']
# questions=['Who developed Slack?','Who was Vincent van Gogh inspired by?']
# questions=['Who is the president of Eritrea?','Who is the mayor of Paris?','Who are the developers of DBpedia']
# questions=['What is in a chocolate chip cookie? ','What is the atmosphere of the Moon composed of?','What is the capital of Cameroon? ','What country is Sitecore from?']
# questions=['What is full name of Prince Charles?','What is Batman’s real name?']

##=====================unprocessed
# questions = ['Show me all books in Asimov’s Foundation series.']
# questions= ['How many moons does Mars have?','How many people live in Poland?','How much did the Lego Movie cost?','How many movies did Park Chan-wook direct?' ,'How many calories does a baguette have?']
# questions=[ 'How many emperors did China have?', 'How did Michael Jackson die?']


# questions=[  'What languages do they speak in Pakistan?','What is Elon Musk famous for?','What is Batman’s real name?','What form of government does Russia have?','What kind of music did Lou Reed play?']
# questions=['What color expresses loyalty?','What are the five boroughs of New York?','What are the zodiac signs?']

# questions=['Which actors play in Big Bang Theory?', 'In which time zone is Rome?']
# questions=['On which day is Columbus Day?', 'Who played Gus Fring in Breaking Bad?']

# questions=['What languages do they speak in Pakistan?','What form of government does Russia have?']
# questions=['Show me all U.S. states']

# ' Did Elvis Presley have children?'
# questions=['Does Neymar play for Real Madrid?', 'Did Kaurismäki ever win the Grand Prix at Cannes?' ]
# questions=['What form of government does Russia have?','Which films did Stanley Kubrick direct?','Which companies produce hovercrafts?']
# questions=[ 'In which ancient empire could you pay with cocoa beans?']
# questions=['Which space probes were sent into orbit around the sun?']
# questions=['What movies does Jesse Eisenberg play in?','Who is the king of the Netherlands?']

######### our dataset
# , 'What is the official language of turkey ?','What is the full name of turkey?', What is the species of royal Bengal tiger?', 'What is the nick name of Ahsanullah University of Science and Technology?','What is the currency code of Turkey?', "What is the birth name of  Nina Pillard?",'How many goals given by Maradona in total?','How many runs scored by Shakib Al Hasan in total?','What is the bowling average of Shakib Al Hasan?','What is the top score of Shakib Al Hasan?',,'How many wickets are taken by Shakib Al Hasan at maximum?','What is the batting average of  Shakib Al Hasan?'
# 'Where  is Ahsanullah University of Science and Technology located?','When was Maynamati War Cemetery  established ?','Where was Shakib Al Hasan born?' 'Where  was Maynamati War Cemetery established ?','Where was Kazi Nazrul Islam born?'
# questions=['which is the fastest growing religion?']
# questions= ['When was 7-up invented?', 'When was Anne Wojcicki born ?','When does the ottoman state founded?','When does the ottoman state end?','When was Comilla city established ?','When was Maynamati War Cemetery  established ?','When was Ahsanullah University of Science and Technology established ?','When was Nina Pilard born?']
# 'Show me the universities of Bangladesh ?', 'Show the broadcast channels of Bangladesh?','How many 100s/50s  has got Sakib Al Hasan  in his carier?'
# questions=['How many matches Sakib Al Hasan played?',How many undergraduates study in  Ahsanullah University of Science and Technology?','How has Kazi Nazrul Islam been influenced in writing rebel poem?']
# questions=['How many movies did Park Chan-wook direct?','How many headquarters are in Dhaka?']

questions = []

urlInputFile = "D:\All Codes and Projects\Python\Resources\Questions - Sheet1.csv"
urlOutputFile = "D:\All Codes and Projects\Python\Resources\ProcessingTime.csv"
question_count = 0

total_qp_time = 0
# qp refers to question processing
qp_time_automation = 0
qp_time_automation_start = 0
qp_time_automation_end = 0
qp_time_dd_start = 0
qp_time_dd_end = 0
total_qp_time_automation = 0
total_qp_time_dd = 0
total_mapping_and_ans_retrieval_time = 0
total_property_time = 0

try:
    inputFile = open(urlInputFile, "r")
    for line in inputFile:
        questions.append(line)

except:
    print("error opening input file")

finally:
    inputFile.close()

try:
    outputFile = open(urlOutputFile, "w")
    outputFile.write("Question Processing Time (s),Query Generation and Answer Retrieval Time (s)")
except:
    print("error opening output file")

for question in questions:
    question_count = question_count + 1
    print(f"Question no: {question_count}")
    # if question_count < 16:
    # continue
    print(question)
    # print("Step 1: Name Entity finding")
    # TODO: start question processing count here
    total_qp_time = time.time()
    nameEntityList = name_entity.getNameEntity(question)
    #    for nameEntity in nameEntityList:
    #        print(nameEntity.text)

    if len(nameEntityList) > 0:
        # print("Step 2: Resource Name finding")
        resourceList = resource_name.getResourceName(nameEntityList)
        # print(resourceList)

        if len(resourceList) > 0:
            # print("Step 3: Keywords finding")
            # finding keyword list by build in services
            total_qp_time = time.time() - total_qp_time
            qp_time_automation_start = time.time()
            keywordListByAM = byAutomation.findKeywordByAutomation(question)
            qp_time_automation_end = time.time()
            total_qp_time_automation = qp_time_automation_end - qp_time_automation_start
            # print(keywordListByAM)

            # finding keyword list by DataDictionary approach
            qp_time_dd_start = time.time()
            keywordListByDD = byDataDictionary.find_keyword_by_dataDictionary(question)
            qp_time_dd_end = time.time()
            total_qp_time_dd = qp_time_dd_end - qp_time_dd_start
            # print(keywordListByDD)

            keywordList = []
            for i in keywordListByDD:
                keywordList.append(i)
            for i in keywordListByAM:
                keywordList.append(i)

            # print("Step 4: Property finding")
            # TODO: make it free from internet issues
            total_property_time = time.time()
            propertyList = getPageProperties(resourceList[0])
            propertyList = getActualProperty(keywordList, propertyList)
            total_property_time = time.time() - total_property_time

            # total_qp_time = total_qp_time + (time.time() - qp_time_dd_end)
            total_qp_time = total_qp_time + min(total_qp_time_automation, total_qp_time_dd)

            # for prop in propertyList:
            #   print(prop.label)

            if len(propertyList) > 0:
                # print("Step 5.0.1: Get Sparql Query IDs")
                questionType = question_type_extraction.findQuestionType(question)
                queryIDs = mysql_operations.findSparqlQueryID(questionType)

                total_mapping_and_ans_retrieval_time = time.time()
                # print("Step 5: All possible answer finding")
                answerArray = api_dbpedia.getQueryResult(propertyList, resourceList, queryIDs, question)
                # print(answerArray)

                # print("Step 6: Answer type extraction")
                questionType = answer_type_extraction.printAnswerType(question, keywordList)
                # print("Expected Answer Type : " + questionType)
                total_mapping_and_ans_retrieval_time = time.time() - total_mapping_and_ans_retrieval_time

                # print("Step 7: Answer type validation")
                answer = answer_validation.answerValidation(answerArray, questionType)
                # print("Actual Answer: " + answer)

            else:
                # print("No property found! Can't go forward without property")
                do_nothing = True
                total_mapping_and_ans_retrieval_time = -1

        else:
            total_qp_time = time.time() - total_qp_time

    else:
        total_qp_time = -1
    # print('\n\n\n')
    total_qp_time_automation = round(total_qp_time_automation, 2)
    total_qp_time_dd = round(total_qp_time_dd, 2)
    total_qp_time = round(total_qp_time, 2)
    total_mapping_and_ans_retrieval_time = round(total_mapping_and_ans_retrieval_time, 2)
    print("qp_by_aut  qp_by_dd  total_qp  map_ans_time")
    print(
        f"\t{total_qp_time_automation} \t {total_qp_time_dd} \t {total_qp_time} \t {total_mapping_and_ans_retrieval_time}")
    # print(f"property finding time: {round(total_property_time, 2)}\n\n")
    outputFile.write(f"{total_qp_time},{total_mapping_and_ans_retrieval_time}")

outputFile.close()
