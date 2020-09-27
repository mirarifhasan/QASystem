import spacy

minSimilarity = 0.55

lang = 'en_core_web_lg'
nlp = spacy.load(lang)

myWord = [('hi', 'hello'), ('buy', 'sell'), ('president', 'leader')]

for i in range(0, len(myWord), 1):
    first = nlp(myWord[i][0])
    second = nlp(myWord[i][1])

    match = first.similarity(second)

    print(myWord[i][0] + ' ~ ' + myWord[i][1] + " : " + str(match))
