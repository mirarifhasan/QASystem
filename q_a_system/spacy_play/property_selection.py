import spacy
from q_a_system.global_pack import constant


def getActualProperty(keywordList, propertyList):
    nlp = spacy.load(constant.lang)
    minSimilarity = constant.minSimilarity
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
