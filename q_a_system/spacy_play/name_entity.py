from q_a_system.global_pack import constant

import spacy


class NameEntity:
    def __init__(self, text, label_):
        self.text = text
        self.label_ = label_


def getNameEntity(question):
    # doc = constant.nlp(question)
    array = []
    question = question.replace("'s", '')

    for i in ['en_core_web_lg', 'en_core_web_sm']:
        nlp = spacy.load(i)
        doc = nlp(question)

        for ent in doc.ents:
            # print(ent.text, ent.start_char, ent.end_char, ent.label_)
            nameEntity = NameEntity(ent.text, ent.label_)
            if nameEntity.text not in [ne.text for ne in array]:
                array.append(nameEntity)

        if len(array) <= 0:
            for chunk in doc.noun_chunks:
                nameEntity = NameEntity(chunk.text, 'PERSON')
                if nameEntity.text not in [ne.text for ne in array]:
                    array.append(nameEntity)

    return array
