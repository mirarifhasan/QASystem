from q_a_system.spacy_play import keyword_extraction


def findKeywordByAutomation(question):
    keywordList = keyword_extraction.getAllKeywords(question)
    # removeNounChunks(question, keywordList)
    return keywordList
