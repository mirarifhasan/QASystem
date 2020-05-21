import spacy
from q_a_system.global_pack import strings

def AllKeywords(question):
    nlp = spacy.load(strings.lang)
    question = nlp(question)

    #print("\nKeyword:")
    keyword = []

    for word in question:
        if (word.is_stop == False) and ((word.pos_) != 'PUNCT') and ((word.text) != '\n'):
            keyword.append(word.text)
    #print(keyword)
    return keyword

