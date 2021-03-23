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
    index = link.find(wiki_link)
    if index == -1:
        # print('no wiki link found')
        return resource
    index = index + len(wiki_link)
    for i in range(index, len(link)):
        character = link[i]
        if character.isalpha() or character == '_' or character == '(' or character == ')' or character == '-':
            resource = resource + character
        else:
            break
    # print("R is", resource)
    return resource


def getResourceNameByGoogleSearch(stringList):
    # for i in stringList:
    links = ["https://www.google.com/search?q=" + stringList]
    # print(links[0])
    page = requests.get(links[0])

    soup = BeautifulSoup(page.content, 'html.parser')

    out_file = open("web_response.txt", "w", encoding='utf-8')

    out_file.write(soup.prettify())

    containers = soup.find_all('a')
    for tag in containers:
        response_link = tag.get('href')

        resource = get_resource_name(response_link)
        # print(f'Obtained resource: {resource}')

        if (resource != ''):
            arr = []
            arr.append(resource)
            return arr
            # return resource.split()
            # print(resource)
            # print("______________________________")
            break

    arr = []
    return arr.append(resource)
