import spacy

def printAllWordDetails(question):
    nlp = spacy.load('en')
    question = nlp(question)

    for token in question:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                token.shape_, token.is_alpha, token.is_stop)