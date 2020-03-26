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

#print (doc_file)
for questions in doc_file.sents:
    print(questions)
    