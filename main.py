from q_a_system.spacy_play import name_entity, resource_name, parts_of_speech

# question = input.getUserQuestion()
question = 'When Obama born?'

nameEntityArray = name_entity.getNameEntity(question)

# parts_of_speech.printAllWordDetails(question)

if len(nameEntityArray) > 0:
    resourceList = resource_name.getResourceName(nameEntityArray)
    print(resourceList)