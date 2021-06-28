import re

#from q_a_system.global_pack import constant
from q_a_system.spacy_play import parts_of_speech
import spacy

def answerValidation(answerArray, questionType,question):
    lang = 'en_core_web_lg'
    nlp = spacy.load(lang)
    dummy_ans_arr = []
    for item in answerArray:
        if item is None:
            continue
        dummy_ans_arr.append(item)

    answerArray = dummy_ans_arr

    if len(answerArray) > 0:
        if questionType == 'NUMBER':
            for answerGroup in answerArray:
                try:
                    if len(answerGroup) > 0:
                        for i in answerGroup:
                            i =i.replace("+","")
                            sentence =nlp(i)
                            for token in sentence.ents:
                                print(token.text, token.label_)
                                if token.label_ in ('PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'):
                                    if (question.find("How many people ") != -1 and (int(i)> 1000) ):
                                        return ' '.join(answerGroup)
                                    elif (question.find("How many") != -1 and (int(i)> 1) ):
                                        return ' '.join(answerGroup)

                except:
                    pass

        # Date pattern matcher
        if questionType == 'DATE':

            # done for coca-cola, 7-up
            if len(answerArray[0]) > 0:
                for i in answerArray[0]:
                    if i.startswith('http') == True:
                        dateRegex4 = re.compile('[a-z]..\d\d\d\d')
                        if dateRegex4.search(i):
                            return "".join(re.findall('\d+', i))

            for answerGroup in answerArray:
                if len(answerGroup) > 0 and answerGroup[0].startswith('http') == False:
                    dateRegex1 = re.compile('\d\d\d\d-\d\d-\d\d')
                    dateRegex2 = re.compile('[a-z]..\d\d\d\d')
                    dateRegex5 = re.compile('[a-z]..I')
                    if dateRegex1.search(answerGroup[0]):
                        return answerGroup[0]
                    if dateRegex5.search(answerGroup[0]):
                        return answerGroup[0]
                    elif dateRegex2.search(answerGroup[0]):
                        return "".join(re.findall('\d+', answerGroup[0]))

            for answerGroup in answerArray:
                if len(answerGroup) > 0 and answerGroup[0].startswith('http') == False:
                    dateRegex3 = re.compile('\d\d-\d\d-\d\d\d\d')
                    dateRegex4 = re.compile('\d\d\d\d')
                    if dateRegex3.search(answerGroup[0]) or dateRegex4.search(answerGroup[0]):
                        return answerGroup[0]

        # person - whom +who
        a = []
        grouparray = []
        flag1 = 0
        flag2 = 0
        singular =0
        if questionType == 'PERSON':
            pos, tag = parts_of_speech.printAllWordDetails(question)
            if (pos == 'AUX' and tag == 'VBZ'):
                singular = 1
            if singular == 1:
                for answerGroup in answerArray:
                    if len(answerGroup) ==1:
                        for i in answerGroup:
                            if i.startswith('http') == True:
                                url_answer = i.split('/')[-1]

                                a = url_answer.split('_')
                                a= ' '.join(a)
                                print(a)
                                grouparray.append(' '.join(a))

                                #sentence = constant.nlp(a)
                                nlp = spacy.load('en_core_web_lg')
                                sentence = nlp(a)
                                for token in sentence.ents:
                                    print(token.text, token.label_)
                                    if token.label_ == questionType or token.label_ in ('PERSON'):
                                        return a
                                        #flag1 = 1
                                        # return ' '.join(url_answer.split('_')) # answer is splited by space
                            else:
                                sentence = nlp(i)
                                for token in sentence.ents:
                                    print(token.text, token.label_)
                                    if token.label_ == questionType or token.label_ in ('PERSON'):
                                        return i



                #return ', '.join((grouparray)) + "(partially)"


            else:
                for answerGroup in answerArray:
                    if len(answerGroup) > 0:
                        for i in answerGroup:
                            if i.startswith('http') == True:
                                url_answer = i.split('/')[-1]
                                a = url_answer.split('_')
                                # a= ' '.join(a)
                                print(a)
                                grouparray.append(' '.join(a))
                                for i in a:
                                    sentence = nlp(i)

                                    for token in sentence.ents:
                                        print(token.text, token.label_)
                                        if token.label_ == questionType or token.label_ in ('ORG', 'PRODUCT', 'PERSON'):
                                            flag1 = 1
                                            # return ' '.join(url_answer.split('_')) # answer is splited by space
                            else:
                                sentence = nlp(i)
                                for token in sentence.ents:
                                    print(token.text, token.label_)
                                    if token.label_ == questionType or token.label_ in ('ORG', 'PRODUCT', 'PERSON'):
                                        return i


                        if a:
                            flag2 = 1
                            # return ' '.join(a) + "(partially)"
                        if flag1 == 1:
                            return ', '.join((grouparray))
                        elif flag2 == 1:
                            return ', '.join((grouparray)) + "(partially)"

        # person - where
        a = []
        grouparray = []
        flag1 = 0
        flag2 = 0
        if questionType == 'LOCATION':
            for answerGroup in answerArray:
                try:
                    if len(answerGroup) > 0:
                        for i in answerGroup:
                            if i.startswith('http') == True:
                                url_answer = i.split('/')[-1]
                                a = url_answer.split('_')
                                # a= ' '.join(a)
                                print(a)
                                grouparray.append(' '.join(a))
                                for i in a:
                                    sentence = nlp(i)

                                    for token in sentence.ents:
                                        print(token.text, token.label_)
                                        if token.label_ == questionType or token.label_ in ('FAC', 'ORG', 'GPE', 'LOC'):
                                            flag1 = 1
                                            # return ' '.join(url_answer.split('_')) # answer is splited by space
                        if a:
                            flag2 = 1
                            # return ' '.join(a) + "(partially)"
                        if flag1 == 1:
                            return ', '.join((grouparray))
                        elif flag2 == 1:
                            return ', '.join((grouparray)) + "(partially)"
                except:
                    pass

        if questionType == 'YES/NO':
            return str(answerArray[0])

        for answerGroup in answerArray:
            if answerGroup is None:
                continue

            if len(answerGroup) > 0:
                sentence = nlp(answerGroup[0])

                for token in sentence.ents:
                    print(token.text, token.label_)
                    if token.label_ == questionType:
                        return answerGroup[0]
                    if token.label_ in ('PERSON', 'ORG') and questionType == 'PERSON':
                        return answerGroup[0]
                    elif token.label_ in ('FAC', 'ORG', 'GPE', 'LOC') and questionType == 'LOCATION':
                        return answerGroup[0]
                    elif token.label_ in ('NORP', 'FAC', 'ORG', 'GPE', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW',
                                          'LANGUAGE') and questionType == 'RESOURCE':
                        print(token.text, token.label_)
                        return ', '.join(answerGroup)
                    elif token.label_ in (
                            'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL') and questionType == 'NUMBER':
                        print(token.text, token.label_)
                        return ', '.join(answerGroup)

            # resource - what+ which
            a = []
            grouparray = []
            flag1 = 0
            flag2 = 0
            if questionType == 'RESOURCE':
                for answerGroup in answerArray:
                    if len(answerGroup) > 0:
                        for i in answerGroup:
                            if i.startswith('http') == True:
                                url_answer = i.split('/')[-1]
                                a = url_answer.split('_')
                                # a= ' '.join(a)
                                print(a)
                                grouparray.append(' '.join(a))
                                for i in a:

                                    i = i.replace("+", "")

                                    sentence = nlp(i)
                                    for token in sentence.ents:
                                        print(token.text, token.label_)
                                        if token.label_ == questionType or token.label_ in (
                                                'NORP', 'FAC', 'ORG', 'GPE', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW',
                                                'LANGUAGE'):
                                            flag1 = 1
                                            # return ' '.join(url_answer.split('_')) # answer is splited by space


                        if a:
                            flag2 = 1
                            # return ' '.join(a) + "(partially)"
                        if flag1 == 1:
                            return ', '.join((grouparray))
                        elif flag2 == 1:
                            return ', '.join((grouparray)) + "(partially)"

            if questionType == 'LIST':
                for answerGroup in answerArray:
                    qu = question.split(' ')
                    if len(answerGroup) > 1 and '' not in answerGroup:
                        for i in answerGroup:
                            if i.startswith('http') == True:
                                url_answer = i.split('/')[-1]
                                a = url_answer.split('_')
                                # a= ' '.join(a)
                                print(a)
                                grouparray.append(' '.join(a))
                        return ', '.join((grouparray))
                    elif len(answerGroup) >0 and qu[0] == "Show":
                        for i in answerGroup:
                            if i.startswith('http') == True:
                                url_answer = i.split('/')[-1]
                                a = url_answer.split('_')
                                # a= ' '.join(a)
                                print(a)
                                grouparray.append(' '.join(a))
                        return ', '.join((grouparray))

        # return ', '.join(answerArray[0]) + "(partially)"   #answerArray[0][0]
        # todo: design a better solution
        try:
            k=-1
            for answer in answerArray:
                k= k+1
                if len(answer) > 0:
                    return answerArray[k][0] + "(partially)"

        except:
            return 'ERR: I GUESS IT\'S EMPTY ANSWER ARRAY'
    else:
        return "No answer"
#print(answerValidation([['+92'], ['http://dbpedia.org/resource/Telephone_numbers_in_Pakistan'] ], "RESOURCE",  "What is the calling code of Pakistan?") )