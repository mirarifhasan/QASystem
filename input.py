# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 13:35:55 2020

@author: Anika Tanzim 
"""


import spacy
nlp = spacy.load('en')

#reading the question file

myfile= open("questions.txt").read()
doc_file= nlp(myfile)
count=0
#print (doc_file)
for questions in doc_file.sents:
    count=count+1
    print(count,". ",questions)
    
    #parts of speech, tags, dependency
    for tokens in questions:
        print(tokens.text,"     ", tokens.pos_,"    ",tokens.tag_, "    ", tokens.dep_)
    print("\nName Entity: ")
    
    #name entity recognition
    for word in questions.ents:
        print(word.text,word.label_)
     
    print("\nKeyword:")
    keyword=[]
    for word in questions:
        if (word.is_stop == False) and (word.text !="?"):
            keyword.append(word.text)
    print(keyword)
    print("\n\n")
    


    
