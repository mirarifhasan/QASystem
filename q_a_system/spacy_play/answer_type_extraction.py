"""
Answer type can be date, location, number, person, resource, process
"""

from q_a_system.global_pack import constant
from q_a_system.spacy_play import parts_of_speech


def printAnswerType(ques, keyword):
    question = constant.nlp(ques)

    number = ["Height", "Elevation", "Peak", "Population", "Temperature"]
    date = ["Birthdate", "DeathDate", "Date", "Year", "Born", "Die"]
    location = ["Location", "Place"]
    name = ["Nicknames", "Birth", "Name", "nicknames", "birth", "name"]

    questionWord = parts_of_speech.tokenize(question)
    # keyword = k.getAllKeywords(ques)

    questionType = "null"
    if questionWord[0] in ['Who', 'Whom']:
        questionType = "PERSON"

    elif questionWord[0] == 'Where':
        questionType = "LOCATION"

    elif questionWord[0] == 'When':
        questionType = "DATE"

    elif questionWord[0] in ['What', 'Which']:

            if questionWord[1] in number:
                questionType = 'NUMBER'

            elif questionWord[1] in date:
                questionType = 'DATE'

            elif questionWord[1] in location:
                questionType = 'LOCATION'

            elif questionWord[1] in name:
                questionType = 'PERSON'
            else:
                questionType = 'RESOURCE'

    elif questionWord[0] in ['How']:
            if questionWord[1] in ["Few", "Little", "Much", "Many", "Often", "Tall"]:
                questionType = "NUMBER"
            elif questionWord[1] in ["Young", "Old", "Long"]:
                questionType = "DATE"


    elif questionWord[0] in ['In', 'On','To','For','At', 'By', 'From']:
        if questionWord[1] in ['which', 'what']:
            questionType = 'RESOURCE'

    elif questionWord[0] in ['Show', 'List','Give']:
        questionType = 'LIST'

    return questionType
