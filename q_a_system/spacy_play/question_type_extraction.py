from q_a_system.global_pack import constant
from q_a_system.spacy_play import parts_of_speech


def findQuestionType(ques):
    question = constant.nlp(ques)
    questionWord = parts_of_speech.tokenize(question)
    word = ""

    if questionWord[0].lower() in ['how', 'what', 'where', 'when', 'which', 'who', 'whom', 'wist']:
        word = questionWord[0].lower()
    elif questionWord[0].lower() in ['show', 'give','list']:
        word = "list"
    elif questionWord[0].lower() in ['in', 'on', 'to'] and questionWord[1].lower() in ['which', 'what']:
        word = questionWord[1].lower()
    elif questionWord[0].lower() in ['do', 'does', 'did']:
        word = questionWord[1].lower()

    return word

# print(findQuestionType("Where is the time"))
