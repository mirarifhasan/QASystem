"""
Answer type can be date, location, number, person
"""

from q_a_system.global_pack import constant
from q_a_system.spacy_play import parts_of_speech


def printAnswerType(ques, keyword):
    question = constant.nlp(ques)

    number = ["Height", "Elevation", "Peak", "Population", "Temperature"]
    date = ["Birthdate", "DeathDate", "Date", "Year", "Born", "Die"]
    location = ["Location", "Place"]
    name = ["Nicknames", "Birth", "Name"]

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
        for i in range(len(keyword)):
            if keyword[i] in number:
                questionType = 'NUMBER'

            elif keyword[i] in date:
                questionType = 'DATE'

            elif keyword[i] in location:
                questionType = 'LOCATION'

            elif keyword[i] in name:
                questionType = 'NAME'

    elif questionWord[0] in ['How']:
        for i in range(len(keyword)):
            if keyword[i] in ["Few", "Little", "Much", "Many", "Often", "Tall"]:
                questionType = "NUMBER"

            elif keyword[i] in ["Young", "Old", "Long"]:
                questionType = "DATE"

    return questionType
