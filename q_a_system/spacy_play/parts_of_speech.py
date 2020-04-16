import spacy

def printAllWordDetails(question):
    nlp = spacy.load('en')
    question = nlp(question)

    for token in question:
        print(f'{token.text:{12}} {token.lemma_:{12}} {token.pos_:{12}} {token.tag_:{12}} {token.dep_:{12}} {token.shape_:{12}} {token.is_alpha:{12}} {token.is_stop:}')
