'''
Answer type can be date, location, number, person
'''

import spacy
from q_a_system.global_pack import strings
from q_a_system.spacy_play import parts_of_speech, keyword_extraction as k

def printAnswerType(ques):
    nlp = spacy.load(strings.lang)
    question = nlp(ques)

    number = ["Height", "Elevation", "Peak", "Population", "Temperature"]
    date = ["Birthdate", "DeathDate", "Date", "Year", "Born", "Die"]
    location = ["Location", "Place"]
    name = ["Nicknames", "Birth", "Name"]

    questionword = parts_of_speech.tokanize(question)
    keyword = k.AllKeywords(ques)
    #print(questionword[0])

    if (questionword[0] in ['Who','Whom']) :
        type = "PERSON"
        print("Expected Answer Type : " + type)

    elif questionword[0] == 'Where':
        type = "LOCATION"
        print("Expected Answer Type : " + type)

    elif questionword[0] == 'When':
        type = "TIME"
        print("Expected Answer Type : " + type)

    elif questionword[0] in ['What','Which'] :
        for i in range(len(keyword)):
            if keyword[i] in number:
                type = 'NUMBER'
                print("Expected Answer Type : " + type)

            elif keyword[i] in date:
                type = 'TIME'
                print("Expected Answer Type : " + type)

            elif keyword[i] in location:
                type = 'LOCATION'
                print("Expected Answer Type : " + type)

            elif keyword[i] in name:
                type = 'NAME'
                print("Expected Answer Type : " + type)


    elif questionword[0] in ['How']:
        for i in range(len(keyword)):
            if keyword[i] in ["Few", "Little", "Much", "Many", "Often", "Tall"]:
                type = "NUMBER"
                print("Expected Answer Type : " + type)
            elif keyword[i] in ["Young", "Old", "Long"]:
                type = "TIME"
                print("Expected Answer Type : " + type)





