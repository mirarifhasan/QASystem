import spacy


class NameEntity:
    def __init__(self, text, label_):
        self.text = text
        self.label_ = label_


def getNameEntity(question):
    nlp = spacy.load('en')
    sentence = nlp(question)
    array = []

    for token in sentence.ents:
        nameEntity = NameEntity(token.text, token.label_)
        array.append(nameEntity)

    return array