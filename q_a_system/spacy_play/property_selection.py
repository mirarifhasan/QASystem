from q_a_system.global_pack import constant


def removeDuplicates(array):
    temp_array = []
    for i in array:
        if i not in temp_array:
            temp_array.append(i)
    return temp_array


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

    array = removeDuplicates(array)
    array.sort(key=lambda x: x.similarity, reverse=True)
    return array
