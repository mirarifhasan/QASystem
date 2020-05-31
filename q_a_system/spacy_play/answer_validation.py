import spacy
from q_a_system.global_pack import strings

nlp = spacy.load(strings.lang)

def answerValidation(answerArray, type):
    answer = []
    for answerGroup in answerArray:
        sentence = nlp(answerGroup[0])

        for token in sentence.ents:
            #print(token.text, token.label_)
            if(token.label_ == type):
                if(type == 'DATE'):
                    return answerGroup[0]
                else:
                    return answerGroup

    return "No result found"
