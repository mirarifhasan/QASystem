import spacy
import mysql.connector
from spacy.matcher import Matcher
from spacy.util import filter_spans
from q_a_system import constant


def get_database():
    selected_database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=constant.DATABASE_NAME
    )
    return selected_database


nlp = spacy.load('en_core_web_sm')
database = get_database()
database_cursor = database.cursor()


def search_for(key, value, table_name):
    query = "SELECT * FROM " + table_name + " WHERE " + key + " = " + value
    database_cursor.execute(query)
    return database_cursor.fetchall()


def find_keyword_by_automation(question):
    keyword_list_by_data_dictionary = []
    matcher = get_matcher()
    doc = nlp(question)
    # call the matcher to find matches
    matches = matcher(doc)
    spans = [doc[start:end] for _, start, end in matches]
    filtered_spans = filter_spans(spans)
    for phrase in filtered_spans:
        result_list = search_for(constant.COLUMN_PHRASE, phrase, constant.TABLE_PHRASE)
        if len(result_list) == 0:
            # i.e phrase not found
            print(phrase + " not found in " + constant.TABLE_PHRASE)
            print("would you like to add it?")
            # TODO: perform insertion operation in phrase table

        else:
            # i.e. phrase found
            for result in result_list:
                phrase_id = result[0]
                relation_list = search_for(constant.COLUMN_PHRASE_ID, phrase_id, constant.TABLE_RELATION)
                if len(relation_list) == 0:
                    # i.e. this phrase do not have keyword
                    print(phrase + ' (phrase id ' + phrase_id + ') does not have corresponding phrase')
                    print('would you like to add corresponding phrase?')
                    choice = input('[y/n]')
                    if choice == 'y':
                        given_keyword = input('enter the phrase')
                        create_relation(phrase_id, given_keyword)
                        keyword_list_by_data_dictionary.append(given_keyword)
                else:
                    # i.e. the phrase has a keyword
                    for relation in relation_list:
                        keyword_id = relation[2]
                        keyword_list = search_for(constant.COLUMN_ID, keyword_id, constant.TABLE_KEYWORD)
                        for row in keyword_list:
                            keyword = row[1]
                            keyword_list_by_data_dictionary.append(keyword)
    return keyword_list_by_data_dictionary


def create_relation(phrase_id, given_keyword):
    relation_list = search_for(constant.COLUMN_KEYWORD, given_keyword, constant.TABLE_KEYWORD)
    if len(relation_list) == 0:
        # TODO: perform insert operation
        print('insert')
        relation_list = search_for(constant.COLUMN_KEYWORD, given_keyword, constant.TABLE_KEYWORD)
    keyword_id = relation_list[0]
    # TODO: insert in relation table


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
