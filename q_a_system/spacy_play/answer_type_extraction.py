"""
Answer type can be date, location, number, person, resource, list
"""

#from q_a_system.global_pack import constant
import spacy
from q_a_system.spacy_play import parts_of_speech


def printAnswerType(ques, keyword):
    plural=0
    pos, tag = parts_of_speech.printAllWordDetails(ques)
    if (pos == 'AUX' and tag== 'VBP'):
        plural=1
    if (pos == 'NOUN' and tag== 'NNS'):
        plural=1
    nlp = spacy.load('en_core_web_lg')
    question = nlp(ques)
    #question = constant.nlp(ques)
    qu = ques.split(' ')
    number = ["height", "elevation", "peak", "population", "temperature","score"]
    date = ["birthdate", "deathDate", "date", "year", "born", "die","day"]
    location = ["location", "place","universities","country", "company", "companies", "city", "river", "school", "University", "country's"]
    name = ["nicknames", "birth", "name", "nicknames", "name?"]
    num_how= ["few", "little", "much", "many", "often", "tall","short"]
    questionWord = parts_of_speech.tokenize(question)
    arr = questionWord[0].split(' ')


    questionType = "null"
    if arr[0] in ['Who', 'Whom','Whose']:
        questionType = "PERSON"

    elif arr[0] == 'Where':
        questionType = "LOCATION"

    elif arr[0] == 'When':
        questionType = "DATE"

    elif arr[0] in ['What', 'Which']:
        if plural ==1:
            questionType='LIST'
        else:
            questionType = 'RESOURCE'
            '''for token in question.ents:
                print(token.text, token.label_)
                if token.label_ == questionType or token.label_ in ('FAC', 'ORG', 'GPE', 'LOC'):
                    questionType = "LOCATION"
                    break '''
            for q in qu:
                if (q in number):
                    questionType = 'NUMBER'
                    break
                elif (q in location ):
                    questionType = 'LOCATION'
                    break
                elif (q in date):
                    questionType = 'DATE'
                    break
                elif (q in name):
                    questionType = 'PERSON'
                    for i in qu:
                        if i in location:
                            questionType = 'LOCATION'
                    break

    elif arr[0] in ['How']:
        if (len(arr)>1 and arr[1] in num_how) or (len(arr)==1 and questionWord[1] in num_how):
            questionType = "NUMBER"
        elif len(arr)>1 and arr[1] in ["Young", "Old", "Long"]:
            questionType = "DATE"
        else:
            questionType = "RESOURCE"

    elif arr[0] in ['In', 'On','To','For','At', 'By', 'From']:
        arr2 = questionWord[1].split(' ')
        if arr2[0] in ['which', 'what']:
            if plural == 1:
                questionType = 'LIST'
            else:
                questionType = 'RESOURCE'
                for q in qu:
                    if (q in number):
                        questionType = 'NUMBER'
                        break
                    elif (q in date):
                        questionType = 'DATE'
                        break
                    elif (q in location):
                        questionType = 'LOCATION'
                        break
                    elif (q in name):
                        questionType = 'PERSON'
                        break
        if arr2[0] in ['whom']:
            questionType = 'PERSON'

    elif arr[0] in ['Show', 'List','Give']:
        if keyword in location:
            questionType = 'LOCATION'
        else:
            questionType = 'LIST'
    elif arr[0] in['Do','Does','Did']:
        questionType = 'YES/NO'

    return questionType
#print(printAnswerType("How short is the shortest active NBA player?",['companies', 'produce', 'hovercrafts']))