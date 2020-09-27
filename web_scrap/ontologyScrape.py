import urllib.request
import csv
from bs4 import BeautifulSoup

baseUrl = 'http://mappings.dbpedia.org/server/ontology/classes/'

urlFile = open('urls.txt', 'r')
urls = urlFile.readlines()
urlFile.close()

file = open("abc.csv", "a", newline='')
writer = csv.writer(file)

for url in urls:
    page = urllib.request.urlopen(baseUrl + url)
    soup = BeautifulSoup(page, 'html.parser')

    rows = soup.find('table', attrs={'border':'1'}).find_all('tr')[1:]
    print(baseUrl + url)
    for row in rows:
        name = str(row.find_all('td')[:1]).split(" ")[1][18:]
        label = str(row.find_all('td')[1:2])[5:-6]

        print(name + '-' + label)
        try:
            writer.writerow([name, label])
        except:
            pass

file.close()