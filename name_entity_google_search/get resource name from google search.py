import requests
from bs4 import BeautifulSoup

def get_resource_name(link):
    resource = ''
    wiki_link = "wikipedia.org/wiki/"
    index = link.find(wiki_link)
    if index == -1:
        return resource
    index = index + len(wiki_link)
    for i in range(index, len(link)):
        character = link[i]
        if character.isalpha() or character == '_' or character == '(' or character == ')':
            resource = resource + character
        else:
            break
    return resource
        
    
links = ["https://www.google.com/search?q=where+does+neymar+play",
         "https://www.google.com/search?q=Park Chan-wook"]
page = requests.get(links[1])

soup = BeautifulSoup(page.content, 'html.parser')

out_file = open("web_response.txt", "w", encoding='utf-8')

out_file.write(soup.prettify())

containers = soup.find_all('a')
for tag in containers:
    response_link = tag.get('href')
    resource = get_resource_name(response_link)
    print(resource)
    print("______________________________")
    

