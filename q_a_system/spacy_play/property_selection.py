from q_a_system.global_pack import constant
from q_a_system.web_scrape import propertyScrape

def removeDuplicates(array):
    temp_array = []
    for i in array:
        if i not in temp_array:
            temp_array.append(i)
    return temp_array


def getActualProperty(keywordList, propertyList, keywordListByDD):
    minSimilarity = constant.minSimilarity
    array = []

    for k in keywordListByDD:
        p1=propertyScrape.Property('dbo',k)
        p1.similarity = 1.0
        array.append(p1)
        p2 = propertyScrape.Property('dbp', k)
        p2.similarity=1.0
        array.append(p2)



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
