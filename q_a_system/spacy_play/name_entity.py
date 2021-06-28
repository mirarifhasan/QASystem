#from q_a_system.global_pack import constant

import spacy


class NameEntity:
    def __init__(self, text, label_):
        self.text = text
        self.label_ = label_


def getNameEntity(question):
    # doc = constant.nlp(question)
    array = []

    if question.find("'s"):
        index = question.find("'s")
        question = [question[:index], question[index + 3:]]
    else:
        question = [question]

    substring = "the"

    for i in ['en_core_web_lg', 'en_core_web_sm']:
        nlp = spacy.load(i)

        for n, q in enumerate(question, start=1):
            doc = nlp(q)

            for ent in doc.ents:
                # print(ent.text, ent.start_char, ent.end_char, ent.label_)
                if substring in ent.text:
                    nameEntity = NameEntity(ent.text[4:], ent.label_)
                else:
                    nameEntity = NameEntity(ent.text, ent.label_)

                if nameEntity.text not in [ne.text for ne in array]:
                    array.append(nameEntity)

            if (len(array) <= 0 and n == 1) or (len(question) == 2 and n == 2):
                for chunk in doc.noun_chunks:
                    if substring in chunk.text:
                        nameEntity = NameEntity(chunk.text[4:], 'PERSON')
                    else:
                        nameEntity = NameEntity(chunk.text, 'PERSON')

                    if nameEntity.text not in [ne.text for ne in array]:
                        array.append(nameEntity)

    notinarray = ["Who", "who", "Which", "which","What", "what", "When", "when", "Where", "where", "How", "how", "Show", "List","Give", "show", "list","give", "you", "You", "ow", "OW"]
    n=[]
    for ar in array:
        for a in notinarray:
            x= ar.text.find(a)
            if x != -1:
                n.append(ar)
                break

    for nn in n:
        array.remove(nn)

    return array

'''x=  getNameEntity("Give the name of skateboarders.")
for xx in x:
    print(xx.text)'''