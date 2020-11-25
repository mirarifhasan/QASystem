import re

from q_a_system.global_pack import constant


def answerValidation(answerArray, questionType):
    # Date pattern matcher
    if questionType == 'DATE':
        for answerGroup in answerArray:
            if len(answerGroup) > 0 and answerGroup[0].startswith('http') == False:
                dateRegex1 = re.compile('\d\d\d\d-\d\d-\d\d')
                dateRegex2 = re.compile('[a-z]..\d\d\d\d')
                dateRegex3 = re.compile('\d\d\d\d$')
                if dateRegex1.search(answerGroup[0]) or dateRegex2.search(answerGroup[0]) or dateRegex3.search(answerGroup[0]):
                    return answerGroup[0]

    #person - whom +who
    a=[]
    grouparray = []
    flag1 = 0
    flag2 = 0
    if questionType == 'PERSON':
        for answerGroup in answerArray:
            if len(answerGroup) > 0:
                for i in answerGroup:
                    if i.startswith('http') == True:
                        url_answer = i.split('/')[-1]
                        a = url_answer.split('_')
                        #a= ' '.join(a)
                        print(a)
                        grouparray.append(' '.join(a))
                        for i in a:
                            sentence = constant.nlp(i)

                            for token in sentence.ents:
                                print(token.text, token.label_)
                                if token.label_ == questionType or token.label_ in ('ORG','PRODUCT','PERSON'):
                                    flag1=1
                                    #return ' '.join(url_answer.split('_')) # answer is splited by space
                                    #return
                if a:
                    flag2=1
                    #return ' '.join(a) + "(partially)"
                if flag1==1:
                    return ', '.join((grouparray))
                elif flag2==1:
                    return ', '.join((grouparray)) + "(partially)"



    #resource - what+ which
    a=[]
    grouparray=[]
    flag1=0
    flag2=0
    if questionType == 'RESOURCE':
        for answerGroup in answerArray:
            if len(answerGroup) > 0:
                for i in answerGroup:
                    if i.startswith('http') == True:
                        url_answer = i.split('/')[-1]
                        a = url_answer.split('_')
                        #a= ' '.join(a)
                        print(a)
                        grouparray.append(' '.join(a))
                        for i in a:
                            sentence = constant.nlp(i)

                            for token in sentence.ents:
                                print(token.text, token.label_)
                                if token.label_ == questionType or token.label_ in ('PERSON','NORP','FAC','ORG','GPE','LOC','PRODUCT','EVENT','WORK_OF_ART','LAW','LANGUAGE','DATE','TIME','PERCENT','MONEY','QUANTITY','ORDINAL','CARDINAL'):
                                    flag1=1
                                    #return ' '.join(url_answer.split('_')) # answer is splited by space

                if a:
                    flag2 = 1
                    #return ' '.join(a) + "(partially)"
                if flag1==1:
                    return ', '.join((grouparray))
                elif flag2==1:
                    return ', '.join((grouparray)) + "(partially)"






    for answerGroup in answerArray:
        if len(answerGroup) > 0:
            sentence = constant.nlp(answerGroup[0])

            for token in sentence.ents:
                print(token.text, token.label_)
                if token.label_ == questionType :
                    return answerGroup[0]
                elif token.label_ in ('FAC','ORG','GPE','LOC') and questionType == 'LOCATION':
                    return ', '.join(answerGroup)
                elif token.label_ in ('PERSON','NORP','FAC','ORG','GPE','LOC','PRODUCT','EVENT','WORK_OF_ART','LAW','LANGUAGE','DATE','TIME','PERCENT','MONEY','QUANTITY','ORDINAL','CARDINAL') and questionType == 'RESOURCE':
                    return ', '.join(answerGroup)




    return "No result found!"



