import re


def calc(operand1, operand2, operator):
    op1 = float(operand1)
    op2 = float(operand2)
    if operator == '^':
        return op1 ** op2
    if operator == '*':
        return op1 * op2
    if operator == '/':
        return op1 / op2
    if operator == '+':
        return op1 + op2
    if operator == '-':
        return op1 - op2


def calcByIdx(fArray, idx):
    oldFunArray = fArray.copy()
    newFunArray = []
    result = str(calc(oldFunArray[idx - 1], oldFunArray[idx + 1], oldFunArray[idx]))
    for j, value in enumerate(oldFunArray):
        if j == idx or j == idx + 1:
            continue
        if j == idx - 1:
            newFunArray.append(result)
        else:
            newFunArray.append(value)

    return newFunArray




def calculateExpersion(functionArray, xValue):
    found = True
    i = -1
    while i < len(functionArray) and found == True:
        if 'x' in functionArray[i + 1:]:
            i = functionArray.index('x', i + 1)
            found = True
            functionArray[i] = xValue
        else:
            found = False

    # newFunction = calculateOperation(functionArray, '^')
    newFunction = functionArray
    # calculate ^ (from right to left)
    while '^' in newFunction:
        for idx,element in enumerate(newFunction[::-1]):
            if element == '^':
                newFunction = calcByIdx(newFunction, len(newFunction)-idx-1)
                print(newFunction)
                break
    print(newFunction)
    # calculate *, /
    while '*' in newFunction or '/' in newFunction:
        for idx,element in enumerate(newFunction):
            if element == '*' or element == '/':
                newFunction = calcByIdx(newFunction, idx)
                print(newFunction)
                break
    # calculate +, -
    while '+' in newFunction or '-' in newFunction:
        for idx,element in enumerate(newFunction):
            if element == '+' or element == '-':
                newFunction = calcByIdx(newFunction, idx)
                print(newFunction)
                break
    print(newFunction)
    finalResult = newFunction[0]
    return finalResult





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
    return functionElements


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
           "2*8^x^1-4/2*3+70.25*x",
           "43+3.4.23*32",
           "43*34+",
           "*246"]
for fstring in fstrings:
    if(funcStringIsValid(fstring)):
        fExpersionArray = function_parsing(fstring)
        result = calculateExpersion(fExpersionArray, 2)
        print(result)