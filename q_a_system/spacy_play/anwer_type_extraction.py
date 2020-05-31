'''
Answer type can be date, location, number, person
'''

import spacy
from q_a_system.global_pack import strings
from q_a_system.spacy_play import parts_of_speech, keyword_extraction as k

def printAnswerType(ques, keyword):
    nlp = spacy.load(strings.lang)
    question = nlp(ques)

    number = ["Height", "Elevation", "Peak", "Population", "Temperature"]
    date = ["Birthdate", "DeathDate", "Date", "Year", "Born", "Die"]
    location = ["Location", "Place"]
    name = ["Nicknames", "Birth", "Name"]

    questionWord = parts_of_speech.tokanize(question)
    # keyword = k.getAllKeywords(ques)

    type = "null"
    if (questionWord[0] in ['Who','Whom']) :
        type = "PERSON"

    elif questionWord[0] == 'Where':
        type = "LOCATION"

    elif questionWord[0] == 'When':
        type = "DATE"

    elif questionWord[0] in ['What','Which'] :
        for i in range(len(keyword)):
            if keyword[i] in number:
                type = 'NUMBER'

            elif keyword[i] in date:
                type = 'DATE'

            elif keyword[i] in location:
                type = 'LOCATION'

            elif keyword[i] in name:
                type = 'NAME'


    elif questionWord[0] in ['How']:
        for i in range(len(keyword)):
            if keyword[i] in ["Few", "Little", "Much", "Many", "Often", "Tall"]:
                type = "NUMBER"

            elif keyword[i] in ["Young", "Old", "Long"]:
                type = "DATE"

    return type





