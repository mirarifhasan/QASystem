import spacy

def printAllKeywords(question):
    nlp = spacy.load('en')
    question = nlp(question)

    print("\nKeyword:")
    keyword = []

    for word in question:
        if (word.is_stop == False) and ((word.pos_) != 'PUNCT') and ((word.text) != '\n'):
            keyword.append(word.text)
    print(keyword)
    print("\n\n")