from wikipedia import wikipedia
from q_a_system.api_sevice import mysql_operations
import requests
from bs4 import BeautifulSoup


def getResourceName(nameEntityArray):
    array = []
    resource = ''
    questionwords = ["who", "what", "where", "when", "how", "which", "list", "show"]

    for nameEntity in nameEntityArray:
        resDic = mysql_operations.findResource(nameEntity.text)

        if len(resDic) > 0:
            array.append(resDic[0][1])
        else:
            try:
                key = wikipedia.page(nameEntity.text)
                resource = key.url[30:]
                array.append(resource)
            except:
                pass

            if not array or resource == '':
                name_arr = nameEntity.text.split(' ')
                f = 0
                for n in name_arr:
                    n = n.lower()
                    if n in questionwords:
                        f = 1
                if f == 0:
                    name_arr = [x.capitalize() for x in name_arr]
                    array.append('_'.join(name_arr))

    reduceHTTPErrorContent(array)
    return array


def reduceHTTPErrorContent(array):
    for i in array:
        if '%' in i:
            array.remove(i)


def get_resource_name(link):
    resource = ''
    wiki_link = "wikipedia.org/wiki/"
    try:
        index = link.find(wiki_link)
        if index == -1:
            return resource
        index = index + len(wiki_link)
        for i in range(index, len(link)):
            character = link[i]
            if character.isalnum() or character == '_' or character == '(' or character == ')' or character == '-':
                resource = resource + character
            else:
                break
    except:
        return resource

    return resource


def getResourceNameByGoogleSearch(stringList):
    arr = []

    for i in stringList:
        links = ["https://www.google.com/search?q=" + i]
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        page = requests.get(links[0],headers=headers)
        print(f"status code: {page.status_code}")
        soup = BeautifulSoup(page.content, 'html.parser')

        out_file = open("web_response.txt", "w", encoding='utf-8')
        out_file.write(soup.prettify())

        containers = soup.find_all('a')
        for tag in containers:
            response_link = tag.get('href')

            resource = get_resource_name(response_link)

            if resource != '':
                arr.append(resource)
                break

    return arr
