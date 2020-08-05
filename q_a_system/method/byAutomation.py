from q_a_system.spacy_play import name_entity, resource_name, parts_of_speech,keyword_extraction,anwer_type_extraction, answer_validation
from q_a_system.input_output import input
from q_a_system.api_sevice import api_dbpedia
from q_a_system.spacy_play.keyword_extraction import removeNounChunks
from q_a_system.spacy_play.property_selection import getActualProperty
from q_a_system.web_scrape.propertyScrape import getPageProperties
import datetime


def findKeywordByAutomation(question):
    keywordList = keyword_extraction.getAllKeywords(question)
    removeNounChunks(question, keywordList)
    return keywordList