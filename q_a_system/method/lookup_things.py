def getResKeywordString(nameEntity, keyword):
    res_key = ""
    ''' removing unwanted name entity from array'''
    questionWords = ["Who", "What", "Where", "When", "How", "Which", "List", "Show"]
    name_arr = []
    for i in nameEntity:
        aa = i.text.split()
        # aa = i.split()
        for a in aa:
            if a in questionWords:
                break
            else:
                name_arr.append((a))

    '''processing keyword array'''
    key_arr = []
    for i in keyword:
        aa = i.split()
        for a in aa:
            if a not in name_arr:
                key_arr.append((a))  # duplicate removed

    '''making string'''
    if len(name_arr) == 0 and len(key_arr) > 1:
        res_key = key_arr[-2] + ' ' + key_arr[-1]  # ex. columbus day
    if len(name_arr) == 0 and len(key_arr) == 1:
        res_key = key_arr[-1]
    if len(name_arr) == 1:
        res_key = name_arr[-1] + ' ' + key_arr[-1]  # ex. Ceres discovered, China emperors
    if len(name_arr) > 1:
        res_key = name_arr[-2] + ' ' + name_arr[-1]  # bang theory , Liz Taylor

    return res_key

# print(getResKeywordString(['shishu park'], ['director', 'movies', 'park chan-wook', 'direct']))