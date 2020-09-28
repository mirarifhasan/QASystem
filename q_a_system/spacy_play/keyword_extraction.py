import spacy
from q_a_system.global_pack import constant


def getAllKeywords(question):
    question = constant.nlp(question)

    keyword = []

    for word in question:
        if (word.is_stop == False) and (word.pos_ != 'PUNCT') and (word.text != '\n'):
            keyword.append(word.text)

    return keyword


def removeNounChunks(question, keywordList):
    sentence = constant.nlp(question)

    for chunk in sentence.noun_chunks:
        try:
            keywordList.remove(chunk.text)
        except:
            pass
