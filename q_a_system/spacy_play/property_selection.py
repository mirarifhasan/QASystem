from q_a_system.global_pack import constant
from q_a_system.web_scrape import propertyScrape


def removeDuplicates(array):
    temp_array = []
    for i in array:
        if i not in temp_array:
            temp_array.append(i)
    return temp_array


def getActualProperty(keywordList, propertyList):
    minSimilarity = constant.minSimilarity
    actualProperty = []

    for propertyListSingleRes in propertyList:
        array = []

        for property in propertyListSingleRes:
            for keyword in keywordList:
                keyword = constant.nlp(keyword)
                propertyLabel = constant.nlp(property.label)
                propertyProperty = constant.nlp(property.property)

                wordSimilarity = keyword.similarity(propertyLabel)
                if keyword.similarity(propertyProperty) > wordSimilarity:
                    wordSimilarity = keyword.similarity(propertyProperty)

                if minSimilarity < wordSimilarity:
                    b = False
                    for arrayObject in array:
                        if arrayObject.property == property.property:
                            b = True
                            if arrayObject.similarity < wordSimilarity:
                                arrayObject.similarity = wordSimilarity
                    if not b:
                        property.similarity = wordSimilarity
                        array.append(property)

        array = removeDuplicates(array)
        array.sort(key=lambda x: x.similarity, reverse=True)
        actualProperty.append(array)

    return actualProperty


def addAdditionalSet(keywordListByDD):
    array = []
    for k in keywordListByDD:
        array.append(propertyScrape.Property('dbo', k))
        array.append(propertyScrape.Property('dbp', k))

    return array
