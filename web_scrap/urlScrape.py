import urllib.request
from bs4 import BeautifulSoup

url = 'http://mappings.dbpedia.org/server/ontology/classes/'
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

rows = soup.find('li').find_all('a', href=True)
count = 0
for row in rows:
    if(row.text.strip() != 'edit'):
        print(row.text.strip())
        count = count + 1
print(count)