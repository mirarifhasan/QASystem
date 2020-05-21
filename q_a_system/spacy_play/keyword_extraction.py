import spacy
from q_a_system.global_pack import strings


def getAllKeywords(question):
    print(strings.lang)
    nlp = spacy.load(strings.lang)
    merge_nps = nlp.create_pipe("merge_noun_chunks")
    nlp.add_pipe(merge_nps)
    question = nlp(question)

    keyword = []

    for word in question:
        if (word.is_stop == False) and ((word.pos_) != 'PUNCT') and ((word.text) != '\n'):
            keyword.append(word.text)
    return keyword


def removeNounChunks(question, keywordList):
    nlp = spacy.load(strings.lang)
    sentence = nlp(question)

    for chunk in sentence.noun_chunks:
        print(chunk.text)
        keywordList.remove(chunk.text)
    return keywordList


def getActualProperty(keywordList, propertyList):
    nlp = spacy.load(strings.lang)
    keyword = nlp(keywordList[0])

    actualPropIndex = 0
    maxSimilarity = 0

    i = 0
    for property in propertyList:
        prop = nlp(property.label)

        if maxSimilarity < keyword.similarity(prop):
            actualPropIndex = i
            maxSimilarity = keyword.similarity(prop)
        i = i + 1
    return actualPropIndex