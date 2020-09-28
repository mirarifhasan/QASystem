import spacy
from q_a_system.global_pack import constant
import re


def answerValidation(answerArray, questionType):
    # Date pattern matcher
    for answerGroup in answerArray:
        if len(answerGroup) > 0 and answerGroup[0].startswith('http') == False:
            dateRegex1 = re.compile('\d\d\d\d-\d\d-\d\d')
            dateRegex2 = re.compile('a-z..\d\d\d\d')
            if dateRegex1.search(answerGroup[0]) or dateRegex2.search(answerGroup[0]):
                return answerGroup[0]

    for answerGroup in answerArray:
        if len(answerGroup) > 0:
            sentence = constant.nlp(answerGroup[0])

            for token in sentence.ents:
                print(token.text, token.label_)
                if token.label_ == questionType:
                    return answerGroup

    return "No result found"
