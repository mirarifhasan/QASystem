import spacy
from q_a_system.global_pack import constant


def getAllKeywords(question):
    nlp = spacy.load(constant.lang)
    merge_nps = nlp.create_pipe("merge_noun_chunks")
    nlp.add_pipe(merge_nps)
    question = nlp(question)

    keyword = []

    for word in question:
        if (word.is_stop == False) and ((word.pos_) != 'PUNCT') and ((word.text) != '\n'):
            keyword.append(word.text)

    return keyword


def removeNounChunks(question, keywordList):
    nlp = spacy.load(constant.lang)
    sentence = nlp(question)

    for chunk in sentence.noun_chunks:
        try:
            keywordList.remove(chunk.text)
        except:
            pass
    return keywordList
