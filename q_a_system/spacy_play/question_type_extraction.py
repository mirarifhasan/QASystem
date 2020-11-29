from q_a_system.global_pack import constant
from q_a_system.spacy_play import parts_of_speech


def findQuestionType(ques):
    question = constant.nlp(ques)
    questionWord = parts_of_speech.tokenize(question)
    word = ""
    arr=questionWord[0].split(' ')
    arr2=questionWord[1].split(' ')
    if arr[0].lower() in ['how', 'what', 'where', 'when', 'which', 'who', 'whom', 'list']:
        word=arr[0].lower()
    elif arr[0].lower() in ['show', 'give']:
        word = "list"
    elif arr[0].lower() in ['in', 'on', 'to'] and (arr2[0].lower() in ['which', 'what']):
        word = arr2[0].lower()
    elif arr[0].lower() in ['do', 'does', 'did']:
        word = arr[0].lower()

    return word

