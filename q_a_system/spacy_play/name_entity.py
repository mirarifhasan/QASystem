from q_a_system.global_pack import constant


class NameEntity:
    def __init__(self, text, label_):
        self.text = text
        self.label_ = label_


def getNameEntity(question):
    sentence = constant.nlp(question)
    array = []

    for token in sentence.ents:
        nameEntity = NameEntity(token.text, token.label_)
        array.append(nameEntity)

    if len(array) <= 0:
        for chunk in sentence.noun_chunks:
            nameEntity = NameEntity(chunk.text, 'PERSON')
            array.append(nameEntity)

    return array
