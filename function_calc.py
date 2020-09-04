import re


def function_parsing(funcString):
    negative = False
    operator = False
    opIdx_old = -1
    functionElements = []
    for index, char in enumerate(funcString):
        if (index == 0 and char == '-'):
            negative = True
            operator = False
        elif (char in "-+*/^"):
            operator = True
            functionElements.append(funcString[opIdx_old+1:index])
            opIdx_old = index
            functionElements.append(char)
        elif (char in "0123456789."):
            operator = False
        elif (char == 'x'):
            operator = False
    functionElements.append(funcString[opIdx_old+1:index+1])

    print(functionElements)

def funcStringIsValid(funcString):
    found = re.findall("[-+*/^x.0-9]",funcString) # "^-[0-9]+|^[0-9]+|[0-9]+[-+*/^][0-9]+"
    # print(len(found), len(funcString))
    if (len(found) < len(funcString)):
        return False
    start = re.match('^[-x0-9]',funcString)
    if (start == None):
        print("no match start")
        return False
    end = re.findall('[x0-9]$', funcString)
    # print(end)
    if (len(end) == 0):
        print("no match end")
        return False
    operands = re.split('[-+*/^]',funcString)
    # print(operands)
    for operand in operands:
        if operand == '':
            continue
        x = re.fullmatch('(\d+[.]{1}\d+)|x{1}|\d+', operand)
        if x == None:
            return False
        print(x.string)
    return True
    # print(funcString.split('-+*/^'))
    # for element in funcString:
    #     print(element)


fstrings = ["434",
           "-23",
           "234+23533",
           "-323*524",
           "5*x+6",
           "43*3+x",
           "543.53*x^24+640/33",
           "43+3.4.23*32",
           "43*34+",
           "*246"]
for fstring in fstrings:
    if(funcStringIsValid(fstring)):
        function_parsing(fstring)