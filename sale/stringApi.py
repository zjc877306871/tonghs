def changeStr(old, replaceStr):
    str1 = old[:2]
    str2 = old[3:4]
    str = str1 + str2+ replaceStr
    # print(str)
    return str

changeStr('10:31','0')
