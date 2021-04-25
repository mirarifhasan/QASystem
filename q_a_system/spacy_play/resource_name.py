from wikipedia import wikipedia
from q_a_system.api_sevice import mysql_operations
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup


def getResourceName(nameEntityArray):
    array = []
    resource = ''
    questionwords = ["who", "what", "where", "when", "how", "which", "list", "show"]

    with ThreadPoolExecutor(max_workers=10) as executor:
        array = executor.map(callWikipediaPage, [ne.text for ne in nameEntityArray])

    if not array:
        for nameEntity in nameEntityArray:
            name_arr = nameEntity.text.split(' ')
            f = 0
            for n in name_arr:
                if n.lower() in questionwords:
                    f = 1
            if f == 0:
                name_arr = [x.capitalize() for x in name_arr]
                array.append('_'.join(name_arr))

    reduceHTTPErrorContent(list(filter(None, array)))
    return list(dict.fromkeys(array))


def reduceHTTPErrorContent(array):
    pass
    # array = [i for i in array if '%' not in i]


def getResourceNameFromFetchedURL(link):
    resource = ''
    wiki_link = "wikipedia.org/wiki/"
    try:
        index = link.find(wiki_link)
        if index == -1:
            return resource
        index = index + len(wiki_link)
        for i in range(index, len(link)):
            character = link[i]
            if character.isalnum() or character == '_' or character == '(' or character == ')' or character == '-' or character == ',' or character == '.':
                resource = resource + character
            else:
                break
    except:
        pass
    return resource


def scrapGoogleResponse(link):
    link = "https://www.google.com/search?q=" + link
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    page = requests.get(link, headers=headers)
    print(f"status code: {page.status_code}")

    soup = BeautifulSoup(page.content, 'html.parser')
    containers = soup.find_all('a')
    for tag in containers:
        response_link = tag.get('href')
        resource = getResourceNameFromFetchedURL(response_link)

        if resource != '':
            return resource


def getResourceNameByGoogleSearch(stringList):
    arr = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        arr = executor.map(scrapGoogleResponse, stringList)

    return list(dict.fromkeys(list(filter(None, arr))))


def getResourceNameWithString(stringList):
    array = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        array = executor.map(callWikipediaPage, stringList)

    reduceHTTPErrorContent(list(filter(None, array)))
    return list(dict.fromkeys(array))


def callWikipediaPage(data):
    try:
        return wikipedia.page(data).url[30:]
    except:
        pass
