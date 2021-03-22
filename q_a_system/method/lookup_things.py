import spacy
import requests
import xml.etree.ElementTree as ET

from q_a_system.global_pack.constant import nlp


def getResKeywordString(nameEntity, keyword):
    res_key = ""
    ''' removing unwanted name entity from array'''
    questionWords = ["Who", "What", "Where", "When", "How", "Which", "List", "Show"]
    name_arr = []
    for i in nameEntity:
        aa = i.split()
        for a in aa:
            if a in questionWords:
                break
            else:
                name_arr.append((a))

    '''processing keyword array'''
    key_arr = []
    for i in keyword:
        aa = i.split()
        for a in aa:
            if a not in name_arr:
                key_arr.append((a))  # duplicate removed

    '''making string'''
    if len(name_arr) == 0 and len(key_arr) > 1:
        res_key = key_arr[-2] + ' ' + key_arr[-1]  # ex. columbus day
    if len(name_arr) == 0 and len(key_arr) == 1:
        res_key = key_arr[-1]
    if len(name_arr) == 1:
        res_key = name_arr[-1] + ' ' + key_arr[-1]  # ex. Ceres discovered, China emperors
    if len(name_arr) > 1:
        res_key = name_arr[-2] + ' ' + name_arr[-1]  # bang theory , Liz Taylor

    return lookupProcess(res_key)

# print(getResKeywordString(['Mars'], ['moons', 'Mars']))


class Model:
    def __init__(self, nameentity, label, uri, similarity):
        self.nameentity = nameentity
        self.label = label
        self.uri = uri
        self.similarity = similarity


def lookupProcess(str):
    response = requests.get('https://lookup.dbpedia.org/api/search?query=' + str)
    response_body = response.content
    root = ET.fromstring(response_body)

    array = []
    first = nlp(str)

    for child in root:
        label = child.find('Label').text
        uri = child.find('URI').text

        second = nlp(label)
        match = first.similarity(second)

        model = Model(str, label, uri, match)
        array.append(model)

    array.sort(key=lambda x: x.similarity, reverse=True)

    # for a in array:
    #     print(a.similarity, a.nameentity, a.label, a.uri)

    if len(array) == 0:
        return []
    return array[0].uri[28:]