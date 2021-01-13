from wikipedia import wikipedia
from q_a_system.api_sevice import mysql_operations


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

    return array
