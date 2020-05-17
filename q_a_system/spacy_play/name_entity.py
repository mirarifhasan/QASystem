import spacy
from q_a_system.global_pack import strings

class NameEntity:
    def __init__(self, text, label_):
        self.text = text
        self.label_ = label_


def getNameEntity(question):
    nlp = spacy.load(strings.lang)
    sentence = nlp(question)
    array = []

    for token in sentence.ents:
        nameEntity = NameEntity(token.text, token.label_)
        array.append(nameEntity)

    if(len(array)<=0):
        for chunk in sentence.noun_chunks:
            nameEntity = NameEntity(chunk.text, 'PERSON')
            array.append(nameEntity)

    return array