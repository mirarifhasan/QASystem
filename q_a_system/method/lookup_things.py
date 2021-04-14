def getResKeywordString(nameEntity, keyword):
    res_key = ""
    ''' removing unwanted name entity from array'''
    questionWords = ["Who", "What", "Where", "When", "How", "Which", "List", "Show", "who", "what", "where", "when",
                     "how", "which", "list", "show"]

    name_arr_mega = []
    res_key_arr = []
    ent_arr=[]
    for i in nameEntity:
        ent_arr.append(i.text.lower())


    for i in nameEntity:
        name_arr = []
        aa = i.text.split()
        # aa = i.split()
        for a in aa:
            if a in questionWords:
                break
            else:
                name_arr.append((a.lower()))
        name_arr_mega.append(name_arr)

    '''processing keyword array'''
    for name_arr in name_arr_mega:
        key_arr = []
        for i in keyword:
            aa = i.split()
            for a in aa:
                a = a.lower()
                #and a not in ent_arr
                if a not in name_arr and a not in ent_arr:
                    key_arr.append((a))  # duplicate removed

        '''making string'''
        if len(name_arr) == 0 and len(key_arr) > 1:
            res_key = key_arr[-2] + ' ' + key_arr[-1]  # ex. columbus day
        if len(name_arr) == 0 and len(key_arr) == 1:
            res_key = key_arr[-1]
        if len(name_arr) == 1:
            res_key = name_arr[-1] + ' ' + key_arr[-1]  # ex. Ceres discovered, China emperors
        if len(name_arr) >=3:
            res_key = name_arr[-3] + ' ' +name_arr[-2] + ' ' + name_arr[-1]
        elif len(name_arr) > 1:
            res_key = name_arr[-2] + ' ' + name_arr[-1]  # bang theory , Liz Taylor

        substring = "the "
        if substring in res_key:
            res_key = res_key[4:]

        res_key_arr.append(res_key)

    return res_key_arr

#print(getResKeywordString(['Sonny','Cher'], ['son','sonny', 'cher']))
