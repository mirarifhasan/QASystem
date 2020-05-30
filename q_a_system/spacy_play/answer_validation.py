import spacy
from q_a_system.global_pack import strings

nlp = spacy.load(strings.lang)

def answer_validation(answer_array, type):
    for word in answer_array:
        sentence = nlp(word)

        for token in sentence.ents:
            #print(token.text, token.label_)
            if(token.label_ == type):
                answer = token.text

    return answer
