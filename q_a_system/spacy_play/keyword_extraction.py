import spacy
from q_a_system.global_pack import strings



def getAllKeywords(question):
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
        keywordList.remove(chunk.text)
    return keywordList


def getActualProperty(keywordList, propertyList):
    nlp = spacy.load(strings.lang)

    minSimilarity = 0.55
    array = []

    for keyword in keywordList:
        keyword = nlp(keyword)

        for property in propertyList:
            propertyLabel = nlp(property.label)

            if minSimilarity < keyword.similarity(propertyLabel):
                # print(propertyLabel)
                # print(keyword.similarity(propertyLabel))
                array.append(property)

    return array
