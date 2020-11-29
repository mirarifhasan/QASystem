"""
Answer type can be date, location, number, person, resource, process
"""

from q_a_system.global_pack import constant
from q_a_system.spacy_play import parts_of_speech, keyword_extraction


def printAnswerType(ques, keyword):
    question = constant.nlp(ques)

    number = ["Height", "Elevation", "Peak", "Population", "Temperature"]
    date = ["Birthdate", "DeathDate", "Date", "Year", "Born", "Die"]
    location = ["Location", "Place","universities"]
    name = ["Nicknames", "Birth", "Name", "nicknames", "birth", "name"]

    questionWord = parts_of_speech.tokenize(question)
    arr = questionWord[0].split(' ')
    keyword = keyword_extraction.getAllKeywords(ques)

    questionType = "null"
    if arr[0] in ['Who', 'Whom']:
        questionType = "PERSON"

    elif arr[0] == 'Where':
        questionType = "LOCATION"

    elif arr[0] == 'When':
        questionType = "DATE"

    elif arr[0] in ['What', 'Which']:

            if arr[1] in number:
                questionType = 'NUMBER'

            elif arr[1] in date:
                questionType = 'DATE'

            elif arr[1] in location:
                questionType = 'LOCATION'

            elif arr[1] in name:
                questionType = 'PERSON'
            else:
                questionType = 'RESOURCE'

    elif arr[0] in ['How']:
            if arr[1] in ["few", "little", "much", "many", "often", "tall"]:
                questionType = "NUMBER"
            elif arr[1] in ["Young", "Old", "Long"]:
                questionType = "DATE"


    elif arr[0] in ['In', 'On','To','For','At', 'By', 'From']:
        arr2 = questionWord[1].split(' ')
        if arr[0] in ['which', 'what']:
            if arr[1] in number:
                questionType = 'NUMBER'

            elif arr[1] in date:
                questionType = 'DATE'

            elif arr[1] in location:
                questionType = 'LOCATION'

            elif arr[1] in name:
                questionType = 'PERSON'
            else:
                questionType = 'RESOURCE'

    elif arr[0] in ['Show', 'List','Give']:
        if keyword in location:
            questionType = 'LOCATION'
        else:
            questionType = 'LIST'
    elif arr[0] in['Do','Does','Did']:
        questionType ='YES/NO'

    return questionType
