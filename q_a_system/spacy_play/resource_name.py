from wikipedia import wikipedia


def getResourceName(nameEntityArray):
    array = []

    for nameEntity in nameEntityArray:
        try:
            key = wikipedia.page(nameEntity.text)
            resource = key.url[30:]
            array.append(resource)
        except:
            pass

    return array
