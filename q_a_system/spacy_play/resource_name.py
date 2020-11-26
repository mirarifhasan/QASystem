from wikipedia import wikipedia


def getResourceName(nameEntityArray):
    array = []

    resource=''
    questionwords = ["Who", "What", "Where", "When", "How", "Which", "List", "who", "what", "where", "when", "how",
                     "which", "list", "Show", "show"]
    for nameEntity in nameEntityArray:

        try:
            key = wikipedia.page(nameEntity.text)
            resource = key.url[30:]
            array.append(resource)
        except:
            pass

        if not array or resource=='':
            name_arr = nameEntity.text.split(' ')
            f = 0
            for n in name_arr:
                if n in questionwords:
                    f=1
            if f==0:
                name_arr = [x.capitalize() for x in name_arr]
                array.append('_'.join(name_arr))

    return array

