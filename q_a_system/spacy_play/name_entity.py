from q_a_system.global_pack import constant

import spacy


class NameEntity:
    def __init__(self, text, label_):
        self.text = text
        self.label_ = label_


def getNameEntity(question):
    # doc = constant.nlp(question)
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(question)

    array = []
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
        nameEntity = NameEntity(ent.text, ent.label_)
        array.append(nameEntity)

    if len(array) <= 0:
        for chunk in doc.noun_chunks:
            nameEntity = NameEntity(chunk.text, 'PERSON')
            array.append(nameEntity)

    return array
