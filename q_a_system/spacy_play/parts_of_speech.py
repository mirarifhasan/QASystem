import spacy
from q_a_system.global_pack import constant


def printAllWordDetails(question):
    question = constant.nlp(question)

    for token in question:
        print(
            f'{token.text:{12}} {token.lemma_:{12}} {token.pos_:{12}} {token.tag_:{12}} {token.dep_:{12}} {token.shape_:{12}} {token.is_alpha:{12}} {token.is_stop:}')


def tokenize(question):
    array = []
    for token in question:
        array.append(token.text);
    return array;
