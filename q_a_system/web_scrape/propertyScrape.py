import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup


class Property:
    def __init__(self, propertyType, property):
        self.propertyType = propertyType
        self.property = property
        self.label = re.sub(r"(\w)([A-Z])", r"\1 \2", property)
        self.similarity = 0.0


def scrapPropertiesByRes(res):
    notAllowedProperty = ['abstract', 'comment', 'isPrimaryTopicOf', 'primaryTopic', 'sameAs', 'seeAlso',
                          'wasDerivedFrom', 'websiteTitle', 'wikiPageExternalLink', 'wikiPageID', 'wikiPageLength',
                          'wikiPageUsesTemplate', 'wikiPageRevisionID', 'wikiPageWikiLink']

    baseUrl = 'http://dbpedia.org/page/'
    try:
        page = urllib.request.urlopen(baseUrl + res)
        subPropertyArray = []

        soup = BeautifulSoup(page, 'html.parser')
        rows = soup.find('table').find_all('td', class_="property")
        for row in rows:
            row = (row.find('a')).text.strip()
            temp = row.split(':')
            if temp[1] not in notAllowedProperty:
                subPropertyArray.append(Property(temp[0], temp[1]))

        return subPropertyArray
    except:
        pass

def getPageProperties(urls):
    propertyArray = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        propertyArray = executor.map(scrapPropertiesByRes, urls)

    return propertyArray
