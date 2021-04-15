import re
import urllib.request

from bs4 import BeautifulSoup


class Property:
    def __init__(self, propertyType, property):
        self.propertyType = propertyType
        self.property = property
        self.label = re.sub(r"(\w)([A-Z])", r"\1 \2", property)
        self.similarity = 0.0


def getPageProperties(urls):
    propertyArray = []
    notAllowedProperty = ['comment', 'isPrimaryTopicOf', 'primaryTopic', 'sameAs', 'seeAlso', 'wasDerivedFrom', 'websiteTitle', 'wikiPageExternalLink', 'wikiPageLength', 'wikiPageUsesTemplate', 'wikiPageWikiLink']

    for url in urls:
        baseUrl = 'http://dbpedia.org/page/'
        try:
            page = urllib.request.urlopen(baseUrl + url)
            subPropertyArray = []

            soup = BeautifulSoup(page, 'html.parser')
            rows = soup.find('table').find_all('td', class_="property")
            for row in rows:
                row = (row.find('a')).text.strip()
                temp = row.split(':')
                if temp[1] not in notAllowedProperty:
                    subPropertyArray.append(Property(temp[0], temp[1]))

            propertyArray.append(subPropertyArray)
        except:
            pass

    return propertyArray
