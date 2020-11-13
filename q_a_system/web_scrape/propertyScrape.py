import re
import urllib.request

from bs4 import BeautifulSoup


class Property:
    def __init__(self, propertyType, property):
        self.propertyType = propertyType
        self.property = property
        self.label = re.sub(r"(\w)([A-Z])", r"\1 \2", property)
        self.similarity = 0.0


def getPageProperties(url):
    baseUrl = 'http://dbpedia.org/page/'
    page = urllib.request.urlopen(baseUrl + url)
    soup = BeautifulSoup(page, 'html.parser')

    rows = soup.find('table').find_all('td', class_="property")

    propertyArray = []
    for row in rows:
        row = (row.find('a')).text.strip()

        temp = row.split(':')
        propertyArray.append(Property(temp[0], temp[1]))

    return propertyArray
