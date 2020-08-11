import spacy
import mysql.connector
from spacy.matcher import Matcher
from spacy.util import filter_spans

nlp = spacy.load('en_core_web_sm')


def find_keyword_by_automation(question):
    keyword_list_by_data_dictionary = []
    matcher = get_matcher()
    doc = nlp(question)
    # call the matcher to find matches
    matches = matcher(doc)
    spans = [doc[start:end] for _, start, end in matches]
    filtered_spans = filter_spans(spans)
    for keyword in filtered_spans:
        keyword_list_by_data_dictionary.append(keyword)

    return keyword_list_by_data_dictionary


def connect_to_database(database_name):
    selected_database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=database_name
    )
    return selected_database


# host="qasystemdb.c4hfxbeu2kdo.ap-southeast-1.rds.amazonaws.com",
# user="admin",
# password="12345678",


def get_matcher():
    # TODO: update pattern list
    pattern_list = [
        [
            {'POS': 'NOUN', 'OP': '+'}
        ],
        [
            {'POS': 'VERB', 'OP': '+'}
        ],
        [
            {'POS': 'ADJ'},
            {'POS': 'NOUN'}
        ],
        [
            {'POS': 'VERB'},
            {'POS': 'NOUN'}
        ],
        [
            {'POS': 'NOUN'},
            {'POS': 'ADP'},
            {'POS': 'NOUN'}
        ],
    ]
    # instantiate a Matcher instance
    matcher = Matcher(nlp.vocab)
    for pattern in pattern_list:
        matcher.add("Noun phrase", None, pattern)

    return matcher
