#from q_a_system.global_pack import constant
import spacy

def printAllWordDetails(question):
    #question = constant.nlp(question)
    nlp = spacy.load('en_core_web_lg')
    question = nlp(question)

    i=0
    flag = 0
    for token in question:
        #print(
        #   f'{token.text:{12}} {token.lemma_:{12}} {token.pos_:{12}} {token.tag_:{12}} {token.dep_:{12}} {token.shape_:{12}} {token.is_alpha:{12}} {token.is_stop:}')
        if i==0 and token.dep_ == 'prep':
            flag =1
        if i==1 and flag==0:
            return token.pos_,token.tag_
        elif i==2 and flag==1:
            return token.pos_, token.tag_
        else:
            i=i+1


def tokenize(question):
    array = []
    for token in question:
        array.append(token.text)
    return array

#print(printAllWordDetails("In which countries do people speak Japanese?"))
