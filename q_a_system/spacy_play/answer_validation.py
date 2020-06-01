import spacy
from q_a_system.global_pack import constant


def answerValidation(answerArray, questionType):

    for answerGroup in answerArray:
        sentence = constant.nlp(answerGroup[0])

        for token in sentence.ents:
            # print(token.text, token.label_)
            if token.label_ == questionType:
                if questionType in ['DATE']:
                    return answerGroup[0]
                else:
                    return answerGroup

    return "No result found"
