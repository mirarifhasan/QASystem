import re

from q_a_system.global_pack import constant


def answerValidation(answerArray, questionType):
    # Date pattern matcher
    if questionType == 'DATE':
        for answerGroup in answerArray:
            if len(answerGroup) > 0 and answerGroup[0].startswith('http') == False:
                dateRegex1 = re.compile('\d\d\d\d-\d\d-\d\d')
                dateRegex2 = re.compile('[a-z]..\d\d\d\d')
                if dateRegex1.search(answerGroup[0]) or dateRegex2.search(answerGroup[0]) :
                    return answerGroup[0]

    #person - whom +who
    a=[]
    if questionType == 'PERSON':
        for answerGroup in answerArray:
            if len(answerGroup) > 0:
                for i in answerGroup:
                    if i.startswith('http') == True:
                        url_answer = i.split('/')[-1]
                        a = url_answer.split('_')
                        #a= ' '.join(a)
                        print(a)
                        for i in a:
                            sentence = constant.nlp(i)

                            for token in sentence.ents:
                                print(token.text, token.label_)
                                if token.label_ == questionType or token.label_ in ('ORG','PRODUCT'):
                                    return ' '.join(url_answer.split('_')) # answer is splited by space
                if a:
                    return ' '.join(a) + "(partially)"




    for answerGroup in answerArray:
        if len(answerGroup) > 0:
            sentence = constant.nlp(answerGroup[0])

            for token in sentence.ents:
                print(token.text, token.label_)
                if token.label_ == questionType :
                    return answerGroup
                elif token.label_ in ('FAC','ORG','GPE','LOC') and questionType == 'LOCATION':
                    return answerGroup[0]
                elif token.label_ in ('PERSON','NORP','FAC','ORG','GPE','LOC','PRODUCT','EVENT','WORK_OF_ART','LAW','LANGUAGE','DATE','TIME','PERCENT','MONEY','QUANTITY','ORDINAL','CARDINAL') and questionType == 'RESOURCE':
                    return answerGroup




    return "No result found!"



