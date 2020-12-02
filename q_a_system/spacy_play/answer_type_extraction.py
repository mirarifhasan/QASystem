"""
Answer type can be date, location, number, person, resource, list
"""

from q_a_system.global_pack import constant
from q_a_system.spacy_play import parts_of_speech, keyword_extraction


def printAnswerType(ques, keyword):
    question = constant.nlp(ques)
    qu = ques.split(' ')
    number = ["height", "elevation", "peak", "population", "temperature","score"]
    date = ["birthdate", "deathDate", "date", "year", "born", "die"]
    location = ["location", "place","universities"]
    name = ["nicknames", "birth", "name", "nicknames"]

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
        questionType = 'RESOURCE'
        for q in qu:
            if (q in number):
                questionType = 'NUMBER'
                break;
            elif (q in date):
                questionType = 'DATE'
                break;
            elif (q in location ):
                questionType = 'LOCATION'
                break;
            elif (q in name):
                questionType = 'PERSON'
                break;


    elif arr[0] in ['How']:
            if len(arr)>1 and arr[1] in ["few", "little", "much", "many", "often", "tall"]:
                questionType = "NUMBER"
            elif len(arr)>1 and arr[1] in ["Young", "Old", "Long"]:
                questionType = "DATE"
            else:
                questionType = "RESOURCE"

    elif arr[0] in ['In', 'On','To','For','At', 'By', 'From']:
        arr2 = questionWord[1].split(' ')
        if arr2[0] in ['which', 'what']:
            questionType = 'RESOURCE'
            for q in qu:
                if (q in number):
                    questionType = 'NUMBER'
                    break;
                elif (q in date):
                    questionType = 'DATE'
                    break;
                elif (q in location):
                    questionType = 'LOCATION'
                    break;
                elif (q in name):
                    questionType = 'PERSON'
                    break;

    elif arr[0] in ['Show', 'List','Give']:
        if keyword in location:
            questionType = 'LOCATION'
        else:
            questionType = 'LIST'
    elif arr[0] in['Do','Does','Did']:
        questionType ='YES/NO'

    return questionType
