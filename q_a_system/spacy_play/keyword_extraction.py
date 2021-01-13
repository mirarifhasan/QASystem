from q_a_system.global_pack import constant


def getAllKeywords(question):
    question = constant.nlp(question)

    ### this is added to solve the problem when "the mayor","what language" gets as keyword, it doesn't match the property. by this we get "mayor","language" as keyowrd.

    questionwords = ["who", "what", "where", "when", "how", "which", "list", "whose"]
    commonwords = ["the", "a", "an", "is", "are", "were", "can", "could", "would", "does", "has", "was", "had", "have", "did", "will", "as", "do", "many", "much"]
    keyword = []

    for word in question:
        if (word.is_stop == False) and (word.pos_ != 'PUNCT') and (word.text != '\n'):
            w = word.text
            ar = w.split(' ')
            arr = []
            for i in ar:
                i = i.lower()
                if (i not in questionwords) and (i not in commonwords):
                    arr.append(i)
                    # keyword.append(i)
            keyword.append(' '.join(arr))

    return keyword


def removeNounChunks(question, keywordList):
    sentence = constant.nlp(question)

    for chunk in sentence.noun_chunks:
        try:
            keywordList.remove(chunk.text)
        except:
            pass
