import spacy
from q_a_system.global_pack import constant


def getActualProperty(keywordList, propertyList):
    minSimilarity = constant.minSimilarity
    array = []

    for keyword in keywordList:
        keyword = constant.nlp(keyword)

        for property in propertyList:
            propertyLabel = constant.nlp(property.label)

            # print(property.label)
            # print(keyword.similarity(propertyLabel))
            wordSimilarity = keyword.similarity(propertyLabel)
            if minSimilarity < wordSimilarity:
                # print(propertyLabel)
                # print(keyword.similarity(propertyLabel))
                property.similarity = wordSimilarity
                array.append(property)

    return array
