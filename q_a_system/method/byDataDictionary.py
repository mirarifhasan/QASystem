import spacy
import mysql
import mysql.connector
from spacy.matcher import Matcher
from spacy.util import filter_spans

from q_a_system import constant as const


# TODO: REMOVE REDUNDANT PRINT STATEMENTS


def get_database():
    selected_database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=const.DATABASE_NAME
    )
    return selected_database


nlp = spacy.load('en_core_web_sm')
database = get_database()
database_cursor = database.cursor()


# the following function will be called in main.py
def find_keyword_by_automation(question):
    print('______________________________find_keyword_by_automation START')
    keyword_list_by_data_dictionary = []
    matcher = get_matcher()
    doc = nlp(question)
    # call the matcher to find matches
    matches = matcher(doc)
    spans = [doc[start:end] for _, start, end in matches]
    filtered_spans = filter_spans(spans)
    for phrase in filtered_spans:
        result_list = search_for(const.COLUMN_PHRASE, phrase, const.TABLE_PHRASE)
        print(f'result list : {result_list}')
        if len(result_list) == 0:
            # i.e phrase not found
            print(f'{phrase} " not found in " {const.TABLE_PHRASE}')
            print("would you like to add it?")
            # TODO: perform insertion operation in phrase table and change logic accordingly
            print("this functionality has not been implemented yet")

        else:
            # i.e. phrase found
            for result in result_list:
                phrase_id = result[0]
                relation_list = search_for(const.COLUMN_PHRASE_ID, phrase_id, const.TABLE_RELATION)
                if len(relation_list) == 0:
                    # i.e. this phrase do not have keyword
                    print(f'{phrase} (phrase id : {phrase_id}) does not have corresponding keyword')
                    print('would you like to add corresponding keyword?')
                    choice = input('[y/n]\n')
                    if choice == 'y':
                        given_keyword = input('enter the keyword\n')
                        create_relation(phrase_id, given_keyword)
                        keyword_list_by_data_dictionary.append(given_keyword)
                        break

                # the phrase is sure to have a keyword
                print(f'relation list : {relation_list}')
                for relation in relation_list:
                    keyword_id = relation[2]
                    keyword_list = search_for(const.COLUMN_ID, keyword_id, const.TABLE_KEYWORD)
                    for row in keyword_list:
                        keyword = row[1]
                        keyword_list_by_data_dictionary.append(keyword)

    print('______________________________find_keyword_by_automation END')
    return keyword_list_by_data_dictionary


def search_for(column_name, value, table_name):
    query = f"SELECT * FROM {table_name} WHERE {column_name} = '{value}'"
    print(f'executed query: {query}')
    database_cursor.execute(query)
    return database_cursor.fetchall()


def create_relation(phrase_id, given_keyword):
    keyword_list = search_for(const.COLUMN_KEYWORD, given_keyword, const.TABLE_KEYWORD)
    if len(keyword_list) == 0:
        # i.e. the given keyword is not available in keyword table
        insert_single_value(const.COLUMN_KEYWORD, given_keyword, const.TABLE_KEYWORD)
        keyword_list = search_for(const.COLUMN_KEYWORD, given_keyword, const.TABLE_KEYWORD)
        if len(keyword_list) == 0:
            print('something is fishy')
            # return
    print(f'keyword_list : {keyword_list}')
    keyword_id = keyword_list[0][0]
    insert_double_value(
        const.COLUMN_PHRASE_ID, const.COLUMN_KEYWORD_ID,
        int(phrase_id), int(keyword_id),
        const.TABLE_RELATION
    )


def insert_single_value(column_name, value, table_name):
    query = f"INSERT INTO {table_name} ({column_name}) VALUES (%s)"
    print(f'executed query: {query}')
    database_cursor.execute(query, value)
    database.commit()


# TODO: merge the two insert functions into one
def insert_double_value(column1, column2, value1, value2, table_name):
    query = f'INSERT INTO {table_name} ({column1}, {column2}) VALUES (%s, %s)'
    print(f'executed query: {query}')
    value = (str(value1), str(value2))
    database_cursor.execute(query, value)
    database.commit()


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
